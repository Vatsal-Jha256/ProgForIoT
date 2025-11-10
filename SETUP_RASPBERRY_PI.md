# Running FedRoute Hardware Demo on Raspberry Pi

Complete step-by-step guide to run the hardware demo on Raspberry Pi with actual hardware components.

## 📋 Prerequisites

- Raspberry Pi (any model with GPIO pins)
- MicroSD card with Raspberry Pi OS installed
- Internet connection for initial setup
- Hardware components (see hardware_setup.md)

## 🔧 Step 1: Initial Raspberry Pi Setup

### 1.1 Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 1.2 Enable Required Interfaces

```bash
sudo raspi-config
```

Navigate and enable:
- **Interface Options → I2C → Enable**
- **Interface Options → SSH → Enable** (optional, for remote access)

Reboot after enabling:
```bash
sudo reboot
```

## 📦 Step 2: Install Python and System Dependencies

### 2.1 Install System Packages

```bash
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-smbus \
    i2c-tools \
    git
```

### 2.2 Verify I2C Connection

```bash
sudo i2cdetect -y 1
```

You should see your OLED display at address `0x3C` (or `3C`).

## 🔌 Step 3: Connect Hardware

Follow the connections in `hardware_setup.md`:

**OLED Display (SSD1306):**
- VCC → 3.3V (Pin 1)
- GND → Ground (Pin 6)
- SCL → SCL (Pin 5)
- SDA → SDA (Pin 3)

**Servo Motor:**
- Red (VCC) → 5V (Pin 2)
- Brown (GND) → Ground (Pin 9)
- Orange (Signal) → GPIO 18 (Pin 12)

**4x4 Keypad:**
- Row 1 → GPIO 23 (Pin 16)
- Row 2 → GPIO 24 (Pin 18)
- Row 3 → GPIO 25 (Pin 22)
- Row 4 → GPIO 8 (Pin 24)
- Col 1 → GPIO 7 (Pin 26)
- Col 2 → GPIO 12 (Pin 32)
- Col 3 → GPIO 16 (Pin 36)
- Col 4 → GPIO 20 (Pin 38)

## 📥 Step 4: Get the Demo Code

### Option A: If you have the hardware_demo folder

```bash
# Navigate to the hardware_demo directory
cd /path/to/IoVFed/hardware_demo
```

### Option B: If you're cloning/copying to a new location

```bash
# Create a directory for the demo
mkdir -p ~/fedroute_hardware_demo
cd ~/fedroute_hardware_demo

# Copy all files from hardware_demo folder:
# - main_demo.py
# - hardware_controller.py
# - demo_*.py files
# - requirements.txt
# - hardware_setup.md
```

## 🐍 Step 5: Set Up Python Environment

### 5.1 Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5.2 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- `RPi.GPIO` - GPIO control
- `adafruit-circuitpython-ssd1306` - OLED display
- `Pillow` - Image processing for OLED text
- `numpy` - Numerical operations

## ✅ Step 6: Test Hardware Connections

### 6.1 Test I2C (OLED)

```bash
sudo i2cdetect -y 1
# Should show 3C for OLED
```

### 6.2 Test Hardware Controller

```bash
python3 hardware_controller.py
```

This will run a basic hardware test. You should see:
- OLED display showing test messages
- Servo moving
- Keypad responding (in simulation mode, it will prompt for input)

## 🚀 Step 7: Run the Demo

### 7.1 Make Script Executable (Optional)

```bash
chmod +x main_demo.py
```

### 7.2 Run the Main Demo

```bash
python3 main_demo.py
```

**Note:** Do NOT use `--simulation` flag when running on actual hardware!

### 7.3 Expected Behavior

1. **Welcome Screen**: OLED shows welcome message, servo animates
2. **Main Menu**: 
   - Press `1` for Federated Learning Demo
   - Press `2` for POI & Navigation Demo
   - Press `3` for System Information
   - Press `*` to exit
3. **During Demos**: 
   - OLED updates with status messages
   - Servo animates to show progress
   - Keypad accepts input

## 🐛 Troubleshooting

### OLED Display Not Working

**Problem:** OLED shows nothing or `i2cdetect` doesn't show 3C

**Solutions:**
```bash
# Check I2C is enabled
sudo raspi-config
# Interface Options → I2C → Enable

# Check wiring
sudo i2cdetect -y 1

# Check permissions (may need to add user to i2c group)
sudo usermod -a -G i2c $USER
# Then logout and login again
```

### Servo Not Moving

**Problem:** Servo doesn't move or jitters

**Solutions:**
- Check power supply (servo needs 5V, may need external power for some servos)
- Verify GPIO 18 connection
- Check if another process is using GPIO 18
- Test with simple script:
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(7.5)  # 90 degrees
time.sleep(2)
pwm.stop()
GPIO.cleanup()
```

### Keypad Not Responding

**Problem:** Keypad doesn't register key presses

**Solutions:**
- Check all row/column connections
- Verify pull-up resistors (keypad should have internal pull-ups)
- Test each connection individually
- Check for loose connections

### Import Errors

**Problem:** `ModuleNotFoundError` for RPi.GPIO or other modules

**Solutions:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall packages
pip install --upgrade -r requirements.txt

# If RPi.GPIO fails, try:
pip install --upgrade RPi.GPIO
```

### Permission Errors

**Problem:** Permission denied for GPIO or I2C

**Solutions:**
```bash
# Add user to gpio and i2c groups
sudo usermod -a -G gpio,i2c $USER

# Logout and login again, or:
newgrp gpio
newgrp i2c
```

## 📝 Running on Boot (Optional)

To run the demo automatically on boot:

### Option 1: Using systemd service

Create `/etc/systemd/system/fedroute-demo.service`:

```ini
[Unit]
Description=FedRoute Hardware Demo
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/fedroute_hardware_demo
Environment="PATH=/home/pi/fedroute_hardware_demo/venv/bin"
ExecStart=/home/pi/fedroute_hardware_demo/venv/bin/python3 main_demo.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable fedroute-demo.service
sudo systemctl start fedroute-demo.service
```

### Option 2: Using .bashrc or autostart

Add to `~/.bashrc`:
```bash
# Run FedRoute demo on login
if [ -z "$SSH_CLIENT" ]; then
    cd ~/fedroute_hardware_demo
    source venv/bin/activate
    python3 main_demo.py
fi
```

## 🎮 Usage Tips

1. **Keypad Navigation:**
   - Keys `1`, `2`, `3` select menu options
   - Key `*` exits
   - Key `A` does NOT work (hardware limitation)
   - Other keys are ignored in menu

2. **During Demos:**
   - Wait for prompts before pressing keys
   - Some demos have timeouts (10-30 seconds)
   - Servo animations indicate progress

3. **Exiting:**
   - Press `*` in main menu to exit gracefully
   - Or press `Ctrl+C` in terminal to force exit

## 📊 Expected Demo Durations

- **Federated Learning Demo**: ~2-3 minutes
- **POI & Navigation Demo**: ~2-3 minutes  
- **System Information**: ~1-2 minutes

## 🔄 Updating the Demo

If you update the code:

```bash
cd ~/fedroute_hardware_demo
git pull  # if using git
# or copy new files

# Reactivate venv if needed
source venv/bin/activate

# Reinstall if requirements changed
pip install -r requirements.txt
```

## 📞 Quick Reference

**Main Commands:**
```bash
# Activate environment
source venv/bin/activate

# Run demo
python3 main_demo.py

# Test hardware
python3 hardware_controller.py

# Check I2C
sudo i2cdetect -y 1
```

**File Locations:**
- Main demo: `main_demo.py`
- Hardware controller: `hardware_controller.py`
- Demo modules: `demo_*.py`
- Requirements: `requirements.txt`
- Setup guide: `hardware_setup.md`

---

**Need Help?** Check `hardware_setup.md` for hardware connection details, or `README.md` for general information.

