#!/usr/bin/env python3
"""
EV Navigation Hardware Controller
Adapted from CA-AMFA hardware controller for EV navigation system
Controls: OLED display, Servo motor (steering), Keypad (input)
"""

import os
import sys
import time
import logging
from typing import Optional, Tuple

# Check if we're running on a Raspberry Pi
IS_RASPBERRY_PI = os.uname().machine.startswith('arm') or os.uname().machine == 'aarch64'
if IS_RASPBERRY_PI:
    try:
        import RPi.GPIO as GPIO
        import board
        import busio
        from adafruit_ssd1306 import SSD1306_I2C
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as e:
        print(f"Warning: Hardware libraries not available: {e}")
        IS_RASPBERRY_PI = False
else:
    print("Not running on Raspberry Pi - using mock hardware controller")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ev_navigation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EVNavigationHardware")


class EVNavigationHardware:
    """Hardware controller for EV navigation system"""
    
    def __init__(self):
        """Initialize hardware components"""
        self.display_available = False
        self.servo_available = False
        
        if IS_RASPBERRY_PI:
            self._init_raspberry_pi()
        else:
            self._init_mock_hardware()
    
    def _init_raspberry_pi(self):
        """Initialize Raspberry Pi hardware"""
        try:
            # Initialize GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Servo Motor (Steering Indicator)
            self.SERVO_PIN = 18  # GPIO 18 (Pin 12)
            GPIO.setup(self.SERVO_PIN, GPIO.OUT)
            self.servo = GPIO.PWM(self.SERVO_PIN, 50)  # 50Hz frequency
            self.servo.start(0)
            self.servo_available = True
            logger.info("✅ Servo motor initialized (GPIO 18)")
            
            # Keypad setup (4x4 Matrix)
            # NOTE: If Row 1 (GPIO 23) doesn't work, try alternative pin like GPIO 5 or GPIO 6
            self.KEYPAD_ROWS = [23, 24, 25, 8]   # GPIO pins
            self.KEYPAD_COLS = [7, 12, 16, 20]   # GPIO pins
            self.KEYPAD_KEYS = [
                ['1', '2', '3', 'A'],
                ['4', '5', '6', 'B'],
                ['7', '8', '9', 'C'],
                ['*', '0', '#', 'D']
            ]
            
            # Setup row pins as outputs with explicit initialization
            row_issues = []
            for i, row in enumerate(self.KEYPAD_ROWS):
                try:
                    GPIO.setup(row, GPIO.OUT, initial=GPIO.HIGH)
                    # Test the pin by toggling it
                    GPIO.output(row, GPIO.LOW)
                    time.sleep(0.01)
                    GPIO.output(row, GPIO.HIGH)
                    logger.info(f"✅ Keypad Row {i+1} (GPIO {row}) initialized")
                except Exception as e:
                    logger.error(f"❌ Failed to initialize keypad Row {i+1} (GPIO {row}): {e}")
                    row_issues.append((i+1, row, str(e)))
            
            if row_issues:
                logger.warning("⚠️  Some keypad rows failed to initialize!")
                for row_num, gpio, error in row_issues:
                    logger.warning(f"   Row {row_num} (GPIO {gpio}): {error}")
                logger.warning("   Check hardware connections. If Row 1 (GPIO 23) doesn't work,")
                logger.warning("   try using GPIO 5 or GPIO 6 as alternative.")
            
            # Setup column pins as inputs with pull-up
            for i, col in enumerate(self.KEYPAD_COLS):
                try:
                    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    logger.info(f"✅ Keypad Col {i+1} (GPIO {col}) initialized")
                except Exception as e:
                    logger.error(f"❌ Failed to initialize keypad Col {i+1} (GPIO {col}): {e}")
            
            # Small delay to ensure pins are stable
            time.sleep(0.1)
            logger.info("✅ Keypad fully initialized")
            
            # OLED Display (SSD1306) - I2C
            try:
                i2c = busio.I2C(board.SCL, board.SDA)
                self.display = SSD1306_I2C(128, 64, i2c)  # 128x64 display
                self.display.fill(0)
                self.display.show()
                self.display_available = True
                logger.info("✅ OLED display initialized (128x64)")
            except Exception as e:
                logger.warning(f"⚠️ OLED display initialization failed: {e}")
                self.display_available = False
                
        except Exception as e:
            logger.error(f"❌ Hardware initialization failed: {e}")
            self.display_available = False
            self.servo_available = False
    
    def _init_mock_hardware(self):
        """Initialize mock hardware for non-Raspberry Pi systems"""
        logger.info("Using mock hardware controller")
        self.display_available = True
        self.servo_available = True
    
    def read_keypad(self) -> Optional[str]:
        """Read input from keypad (non-blocking)"""
        if not IS_RASPBERRY_PI:
            # Mock keypad - simulate input
            import random
            if random.random() < 0.05:  # 5% chance
                return random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '#', '*', 'A', 'B', 'C', 'D'])
            return None
        
        try:
            for row_idx, row in enumerate(self.KEYPAD_ROWS):
                try:
                    # Set current row to LOW
                    GPIO.output(row, GPIO.LOW)
                    time.sleep(0.001)  # Small delay for signal to stabilize
                    
                    for col_idx, col in enumerate(self.KEYPAD_COLS):
                        # Read column state
                        col_state = GPIO.input(col)
                        if col_state == GPIO.LOW:  # Key is pressed
                            key = self.KEYPAD_KEYS[row_idx][col_idx]
                            
                            # Wait for key release (debounce)
                            debounce_count = 0
                            while GPIO.input(col) == GPIO.LOW and debounce_count < 50:
                                time.sleep(0.01)
                                debounce_count += 1
                            
                            GPIO.output(row, GPIO.HIGH)  # Reset row
                            logger.debug(f"Keypad key detected: {key} (Row {row_idx+1}, Col {col_idx+1})")
                            return key
                    
                    # Reset row to HIGH
                    GPIO.output(row, GPIO.HIGH)
                    time.sleep(0.001)  # Small delay between rows
                    
                except Exception as row_error:
                    logger.warning(f"Error reading keypad row {row_idx+1} (GPIO {row}): {row_error}")
                    GPIO.output(row, GPIO.HIGH)  # Ensure row is reset
                    continue
            
            return None
        except Exception as e:
            logger.error(f"Keypad read error: {e}")
            return None
    
    def display_navigation(self, direction: str, distance: float, eta: float, 
                          battery: float, next_station: str = ""):
        """
        Display navigation information on OLED
        
        Args:
            direction: "LEFT", "RIGHT", "STRAIGHT", "ARRIVED"
            distance: Distance in km
            eta: Estimated time in minutes
            battery: Battery percentage (0-100)
            next_station: Next charging station ID
        """
        message = f"Next: {direction}\n"
        message += f"Dist: {distance:.1f} km\n"
        message += f"ETA: {eta:.0f} min\n"
        message += f"Battery: {battery:.0f}%"
        
        if next_station:
            message += f"\nStation: {next_station}"
        
        self.display_message(message)
    
    def display_message(self, message: str):
        """Display text message on OLED display"""
        if IS_RASPBERRY_PI and self.display_available:
            try:
                self.display.fill(0)
                
                # Create blank image for drawing
                image = Image.new("1", (self.display.width, self.display.height))
                draw = ImageDraw.Draw(image)
                
                # Load default font
                font = ImageFont.load_default()
                
                # Split message into lines
                lines = message.split('\n')
                max_lines = min(len(lines), 8)  # Display up to 8 lines (64px / 8px per line)
                
                for i, line in enumerate(lines[:max_lines]):
                    y_pos = i * 8  # 8 pixels per line
                    draw.text((0, y_pos), line, font=font, fill=255)
                
                # Display image
                self.display.image(image)
                self.display.show()
                
            except Exception as e:
                logger.error(f"Display error: {e}")
                print(f"Display (OLED unavailable): {message}")
        else:
            print(f"Display: {message}")
    
    def set_steering(self, direction: str):
        """
        Control servo motor to indicate steering direction
        
        Args:
            direction: "LEFT", "RIGHT", "STRAIGHT", "STOP"
        """
        if not IS_RASPBERRY_PI or not self.servo_available:
            print(f"Mock steering: {direction}")
            return
        
        try:
            # Servo positions (duty cycle for 50Hz PWM)
            # 0° = 2.5% duty cycle (left)
            # 90° = 7.5% duty cycle (center/straight)
            # 180° = 12.5% duty cycle (right)
            
            if direction == "LEFT":
                self.servo.ChangeDutyCycle(2.5)  # Point left
            elif direction == "RIGHT":
                self.servo.ChangeDutyCycle(12.5)  # Point right
            elif direction == "STRAIGHT":
                self.servo.ChangeDutyCycle(7.5)  # Center position
            elif direction == "STOP":
                self.servo.ChangeDutyCycle(0)  # Stop
            else:
                logger.warning(f"Unknown steering direction: {direction}")
                return
            
            time.sleep(0.1)  # Give servo time to move
            
            # Stop servo jitter (only for non-STOP commands)
            if direction != "STOP":
                time.sleep(0.05)
                self.servo.ChangeDutyCycle(0)
                
        except Exception as e:
            logger.error(f"Servo control error: {e}")
    
    def update_steering_from_heading(self, current_heading: float, target_heading: float):
        """
        Update steering based on heading difference
        
        Args:
            current_heading: Current vehicle heading in degrees (0-360)
            target_heading: Target heading in degrees (0-360)
        """
        # Calculate angle difference
        angle_diff = target_heading - current_heading
        
        # Normalize to -180 to 180 range
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
        
        # Determine steering direction
        if abs(angle_diff) < 15:  # Within 15 degrees = straight
            self.set_steering("STRAIGHT")
        elif angle_diff > 0:  # Turn right
            self.set_steering("RIGHT")
        else:  # Turn left
            self.set_steering("LEFT")
    
    def display_station_info(self, station_id: str, distance: float, 
                            availability: str = "Available"):
        """Display charging station information"""
        message = f"Station: {station_id}\n"
        message += f"Distance: {distance:.1f} km\n"
        message += f"Status: {availability}\n"
        message += "Press # to navigate"
        
        self.display_message(message)
    
    def display_menu(self, options: list):
        """Display menu options on OLED"""
        message = "Select option:\n"
        for i, option in enumerate(options[:6], 1):  # Max 6 options
            message += f"{i}. {option}\n"
        
        self.display_message(message)
    
    def cleanup(self):
        """Clean up hardware resources"""
        logger.info("Cleaning up hardware...")
        
        if IS_RASPBERRY_PI:
            try:
                if self.servo_available:
                    self.servo.stop()
                    logger.info("✅ Servo stopped")
            except Exception as e:
                logger.error(f"Error stopping servo: {e}")
            
            try:
                GPIO.cleanup()
                logger.info("✅ GPIO cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning GPIO: {e}")
        
        logger.info("Hardware cleanup complete")


# Test function
if __name__ == "__main__":
    print("Testing EV Navigation Hardware Controller...")
    
    hw = EVNavigationHardware()
    
    try:
        # Test display
        print("\n1. Testing OLED display...")
        hw.display_message("EV Navigation\nSystem Test\nOLED Working")
        time.sleep(2)
        
        # Test navigation display
        print("\n2. Testing navigation display...")
        hw.display_navigation("RIGHT", 2.5, 8, 65, "ST05")
        time.sleep(2)
        
        # Test steering
        print("\n3. Testing servo steering...")
        for direction in ["LEFT", "STRAIGHT", "RIGHT", "STRAIGHT", "STOP"]:
            print(f"   Setting steering to: {direction}")
            hw.set_steering(direction)
            time.sleep(1)
        
        # Test keypad
        print("\n4. Testing keypad (press keys, # to exit)...")
        print("   Testing all rows - press keys from each row:")
        print("   Row 1: 1, 2, 3, A")
        print("   Row 2: 4, 5, 6, B")
        print("   Row 3: 7, 8, 9, C")
        print("   Row 4: *, 0, #, D")
        print("   Press # to exit")
        
        keys_pressed = []
        while True:
            key = hw.read_keypad()
            if key:
                keys_pressed.append(key)
                print(f"   ✅ Key pressed: {key} (Total: {len(keys_pressed)})")
                hw.display_message(f"Key: {key}\nTotal: {len(keys_pressed)}\nPress # to exit")
                
                # Test each row
                if key in ['1', '2', '3', 'A']:
                    print(f"      ✓ Row 1 working! (GPIO 23)")
                elif key in ['4', '5', '6', 'B']:
                    print(f"      ✓ Row 2 working! (GPIO 24)")
                elif key in ['7', '8', '9', 'C']:
                    print(f"      ✓ Row 3 working! (GPIO 25)")
                elif key in ['*', '0', '#', 'D']:
                    print(f"      ✓ Row 4 working! (GPIO 8)")
                
                if key == '#':
                    break
            time.sleep(0.1)
        
        print(f"\n   Keypad test complete! Total keys pressed: {len(keys_pressed)}")
        if len(keys_pressed) > 0:
            print(f"   Keys tested: {', '.join(set(keys_pressed))}")
        
        print("\n✅ All hardware tests completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
    finally:
        hw.cleanup()


