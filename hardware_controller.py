#!/usr/bin/env python3
"""
Hardware Controller for FedRoute Hardware Demo
Manages OLED display, servo motor, and keypad input

Author: FedRoute Team
Date: 2025
"""

import time
import threading
from typing import Optional, Callable
from queue import Queue

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("⚠️  RPi.GPIO not available. Running in simulation mode.")

try:
    from board import SCL, SDA
    import busio
    from adafruit_ssd1306 import SSD1306_I2C
    from PIL import Image, ImageDraw, ImageFont
    OLED_AVAILABLE = True
except ImportError:
    OLED_AVAILABLE = False
    try:
        from PIL import Image, ImageDraw, ImageFont
        PIL_AVAILABLE = True
    except ImportError:
        PIL_AVAILABLE = False
    print("⚠️  OLED libraries not available. Running in simulation mode.")


class HardwareController:
    """
    Controller for hardware components: OLED, Servo, Keypad
    """
    
    def __init__(self, simulation_mode: bool = False):
        """
        Initialize hardware controller.
        
        Args:
            simulation_mode: If True, run without actual hardware (for testing)
        """
        self.simulation_mode = simulation_mode or not GPIO_AVAILABLE
        self.keypad_queue = Queue()
        self.keypad_callback: Optional[Callable] = None
        
        # GPIO pin definitions (from hardware_setup.md)
        self.SERVO_PIN = 18
        self.KEYPAD_ROWS = [23, 24, 25, 8]
        self.KEYPAD_COLS = [7, 12, 16, 20]
        
        # Keypad mapping (4x4 matrix)
        # Note: A key doesn't work, so we map it to None
        self.KEYPAD_MAP = [
            ['1', '2', '3', None],  # Row 0: 1, 2, 3, A (A doesn't work)
            ['4', '5', '6', 'B'],   # Row 1: 4, 5, 6, B
            ['7', '8', '9', 'C'],   # Row 2: 7, 8, 9, C
            ['*', '0', '#', 'D']    # Row 3: *, 0, #, D (D as placeholder)
        ]
        
        # OLED settings
        self.OLED_WIDTH = 128
        self.OLED_HEIGHT = 64
        self.OLED_ADDRESS = 0x3C
        
        # Initialize components
        self._init_gpio()
        self._init_oled()
        self._init_servo()
        self._init_keypad()
        
        print("✅ Hardware Controller initialized")
        if self.simulation_mode:
            print("   Running in SIMULATION MODE")
    
    def _init_gpio(self):
        """Initialize GPIO pins."""
        if not self.simulation_mode:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        else:
            print("   [SIM] GPIO initialized")
    
    def _init_oled(self):
        """Initialize OLED display."""
        if not self.simulation_mode and OLED_AVAILABLE:
            try:
                i2c = busio.I2C(SCL, SDA)
                self.oled = SSD1306_I2C(self.OLED_WIDTH, self.OLED_HEIGHT, i2c, addr=self.OLED_ADDRESS)
                self.oled.fill(0)
                self.oled.show()
                # Create PIL image for text rendering
                self.image = Image.new('1', (self.OLED_WIDTH, self.OLED_HEIGHT))
                self.draw = ImageDraw.Draw(self.image)
                try:
                    self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
                    self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
                except:
                    self.font = ImageFont.load_default()
                    self.font_large = ImageFont.load_default()
                print("   ✅ OLED display connected")
            except Exception as e:
                print(f"   ⚠️  OLED init failed: {e}")
                self.simulation_mode = True
                self.oled = None
                self.image = None
                self.draw = None
        else:
            self.oled = None
            self.image = None
            self.draw = None
            print("   [SIM] OLED display")
    
    def _init_servo(self):
        """Initialize servo motor."""
        if not self.simulation_mode:
            try:
                GPIO.setup(self.SERVO_PIN, GPIO.OUT)
                self.servo_pwm = GPIO.PWM(self.SERVO_PIN, 50)  # 50Hz
                self.servo_pwm.start(0)
                print("   ✅ Servo motor connected")
            except Exception as e:
                print(f"   ⚠️  Servo init failed: {e}")
                self.servo_pwm = None
        else:
            self.servo_pwm = None
            print("   [SIM] Servo motor")
    
    def _init_keypad(self):
        """Initialize keypad."""
        if not self.simulation_mode:
            try:
                # Setup row pins as outputs
                for row in self.KEYPAD_ROWS:
                    GPIO.setup(row, GPIO.OUT)
                    GPIO.output(row, GPIO.LOW)
                
                # Setup column pins as inputs with pull-up
                for col in self.KEYPAD_COLS:
                    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                
                # Start keypad monitoring thread
                self.keypad_running = True
                keypad_thread = threading.Thread(target=self._monitor_keypad, daemon=True)
                keypad_thread.start()
                print("   ✅ Keypad connected")
            except Exception as e:
                print(f"   ⚠️  Keypad init failed: {e}")
                self.keypad_running = False
        else:
            self.keypad_running = True
            print("   [SIM] Keypad")
    
    def _monitor_keypad(self):
        """Monitor keypad for key presses (runs in background thread)."""
        last_key = None
        last_press_time = 0
        debounce_time = 0.2  # 200ms debounce
        
        while self.keypad_running:
            if self.simulation_mode:
                # In simulation, we'll handle keypad input differently
                time.sleep(0.1)
                continue
            
            try:
                key_pressed = None
                
                # Scan keypad matrix
                for row_idx, row_pin in enumerate(self.KEYPAD_ROWS):
                    GPIO.output(row_pin, GPIO.LOW)
                    
                    for col_idx, col_pin in enumerate(self.KEYPAD_COLS):
                        if GPIO.input(col_pin) == GPIO.LOW:
                            key_pressed = self.KEYPAD_MAP[row_idx][col_idx]
                            break
                    
                    GPIO.output(row_pin, GPIO.HIGH)
                    
                    if key_pressed:
                        break
                
                # Handle key press with debouncing
                if key_pressed and key_pressed != last_key:
                    current_time = time.time()
                    if current_time - last_press_time > debounce_time:
                        if key_pressed:  # Only process valid keys (not None)
                            self.keypad_queue.put(key_pressed)
                            if self.keypad_callback:
                                self.keypad_callback(key_pressed)
                            last_press_time = current_time
                        last_key = key_pressed
                elif not key_pressed:
                    last_key = None
                
                time.sleep(0.05)  # Small delay to prevent CPU spinning
                
            except Exception as e:
                print(f"Keypad error: {e}")
                time.sleep(0.1)
    
    def display_message(self, message: str, clear: bool = True):
        """
        Display a message on OLED.
        
        Args:
            message: Text to display (supports \n for newlines)
            clear: Whether to clear display first
        """
        if self.simulation_mode:
            print("\n" + "="*20)
            print("OLED Display:")
            print(message)
            print("="*20 + "\n")
            return
        
        if not self.oled or not self.draw:
            print(f"[OLED] {message}")
            return
        
        try:
            if clear:
                self.draw.rectangle((0, 0, self.OLED_WIDTH, self.OLED_HEIGHT), outline=0, fill=0)
            
            # Split message into lines
            lines = message.split('\n')
            
            # Render text using PIL
            y = 2
            line_height = 10
            
            for line in lines[:7]:  # Max 7 lines for 64px height
                if y >= self.OLED_HEIGHT - line_height:
                    break
                if line.strip():  # Only render non-empty lines
                    self.draw.text((2, y), line.strip(), font=self.font, fill=255)
                y += line_height
            
            # Display on OLED
            self.oled.image(self.image)
            self.oled.show()
        except Exception as e:
            print(f"OLED display error: {e}")
    
    def display_menu(self, title: str, options: list):
        """
        Display a menu on OLED.
        
        Args:
            title: Menu title
            options: List of option strings
        """
        menu_text = f"{title}\n\n"
        for i, option in enumerate(options[:6], 1):  # Max 6 options
            menu_text += f"{i}. {option}\n"
        
        self.display_message(menu_text)
    
    def set_servo_angle(self, angle: float):
        """
        Set servo motor angle.
        
        Args:
            angle: Angle in degrees (0-180)
        """
        if self.simulation_mode:
            print(f"[SERVO] Angle: {angle}°")
            return
        
        if not self.servo_pwm:
            return
        
        try:
            # Convert angle to duty cycle (0° = 2.5%, 180° = 12.5%)
            duty = 2.5 + (angle / 180.0) * 10.0
            self.servo_pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)  # Allow servo to move
        except Exception as e:
            print(f"Servo error: {e}")
    
    def servo_animation(self, start_angle: float, end_angle: float, steps: int = 10, delay: float = 0.05):
        """
        Animate servo movement.
        
        Args:
            start_angle: Starting angle
            end_angle: Ending angle
            steps: Number of animation steps
            delay: Delay between steps
        """
        for i in range(steps + 1):
            angle = start_angle + (end_angle - start_angle) * (i / steps)
            self.set_servo_angle(angle)
            time.sleep(delay)
    
    def get_key(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Get a key press from keypad.
        
        Args:
            timeout: Maximum time to wait (None = wait indefinitely)
            
        Returns:
            Key pressed or None if timeout
        """
        if self.simulation_mode:
            # In simulation, prompt user for input
            try:
                key = input("Enter key (1-9,0,B,C,#,*): ").strip().upper()
                if key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'B', 'C', '#', '*']:
                    return key
                return None
            except:
                return None
        
        try:
            return self.keypad_queue.get(timeout=timeout)
        except:
            return None
    
    def set_keypad_callback(self, callback: Callable[[str], None]):
        """
        Set callback function for keypad presses.
        
        Args:
            callback: Function that takes a key string as argument
        """
        self.keypad_callback = callback
    
    def clear_display(self):
        """Clear OLED display."""
        if not self.simulation_mode and self.oled and self.draw:
            try:
                self.draw.rectangle((0, 0, self.OLED_WIDTH, self.OLED_HEIGHT), outline=0, fill=0)
                self.oled.image(self.image)
                self.oled.show()
            except:
                pass
    
    def cleanup(self):
        """Clean up hardware resources."""
        self.keypad_running = False
        
        if not self.simulation_mode:
            try:
                if self.servo_pwm:
                    self.servo_pwm.stop()
                GPIO.cleanup()
                if self.oled:
                    self.clear_display()
            except:
                pass
        
        print("✅ Hardware cleaned up")


if __name__ == "__main__":
    # Test hardware controller
    controller = HardwareController(simulation_mode=True)
    
    print("\nTesting hardware controller...")
    print("Display test:")
    controller.display_message("FedRoute\nHardware Demo\n\nTesting...")
    time.sleep(1)
    
    print("Servo test:")
    controller.servo_animation(0, 180, 20, 0.05)
    time.sleep(0.5)
    controller.servo_animation(180, 0, 20, 0.05)
    
    print("Keypad test (press keys, or 'q' to quit):")
    controller.set_keypad_callback(lambda key: print(f"Key pressed: {key}"))
    
    start_time = time.time()
    while time.time() - start_time < 10:
        key = controller.get_key(timeout=1.0)
        if key:
            print(f"Got key: {key}")
    
    controller.cleanup()
    print("Test complete!")

