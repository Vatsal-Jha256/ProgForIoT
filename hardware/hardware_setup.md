# Hardware Setup Guide

## Required Components
- Raspberry Pi (any model with GPIO pins)
- OLED Display (SSD1306)
- Servo Motor (SG90 or similar)
- 4x4 Matrix Keypad

## Physical Connections

### 1. OLED Display (SSD1306)
Connect the display to the Raspberry Pi's I2C pins:
- VCC -> 3.3V (Pin 1)
- GND -> Ground (Pin 6)
- SCL -> SCL (Pin 5)
- SDA -> SDA (Pin 3)

### 2. Servo Motor
Connect the servo to GPIO pins:
- Red (VCC) -> 5V (Pin 2)
- Brown (GND) -> Ground (Pin 9)
- Orange (Signal) -> GPIO 18 (Pin 12)

### 3. Matrix Keypad
Connect the keypad to GPIO pins:
```
Row 1 -> GPIO 23 (Pin 16)
Row 2 -> GPIO 24 (Pin 18)
Row 3 -> GPIO 25 (Pin 22)
Row 4 -> GPIO 8 (Pin 24)
Col 1 -> GPIO 7 (Pin 26)
Col 2 -> GPIO 12 (Pin 32)
Col 3 -> GPIO 16 (Pin 36)
Col 4 -> GPIO 20 (Pin 38)
```

## Software Setup

1. Enable I2C:
```bash
sudo raspi-config
# Select Interface Options
# Enable I2C
```

2. Install required packages:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus i2c-tools
sudo pip3 install RPi.GPIO adafruit-circuitpython-ssd1306 Pillow
```

3. Verify I2C connection:
```bash
sudo i2cdetect -y 1
# You should see your OLED display address (usually 0x3C)
```

## Testing the Setup

1. Run the hardware test script:
```bash
cd hardware_demo/hardware
python3 ev_navigation_hardware.py
```

2. Expected behavior:
- Servo should move between positions
- Keypad should register key presses
- OLED display should show test messages

## Troubleshooting

### OLED Display Issues
- Check I2C connection with `i2cdetect -y 1`
- Verify power and ground connections
- Check SCL and SDA connections

### Servo Issues
- Check power supply (servo needs 5V)
- Verify PWM signal connection
- Test with different duty cycles

### Keypad Issues
- Check all row and column connections
- Verify pull-up resistors are working
- Test each key individually

## Next Steps

After successful hardware testing:
1. Run the hardware demo: `cd hardware_demo/demo && python3 run_hardware_demo.py`
2. Test federated learning integration
3. Verify real-time status display
4. Test interactive keypad controls

