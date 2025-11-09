# How to Run the Hardware Demo - Quick Guide

## 🎯 Quick Answer: Does Torch Run on Raspberry Pi?

**YES!** The Hardware FL Client runs on Raspberry Pi and uses **torch** to train federated learning models locally. The Pi needs both:
- **torch + numpy** (for federated learning)
- **Hardware libraries** (RPi.GPIO, adafruit-ssd1306, etc. for physical hardware)

## 📋 What Runs Where?

| Component | Runs On | Needs | Purpose |
|-----------|---------|-------|---------|
| **FL Server** | Any machine | torch, numpy | Coordinates FL, aggregates updates |
| **Hardware Client** | **Raspberry Pi** | torch, numpy + hardware libs | Trains models, controls OLED/Servo/Keypad |
| **Software Clients** | Any machine | torch, numpy | Additional clients for comparison |

## 🚀 Quick Start (All on Raspberry Pi)

### 1. Install Everything
```bash
# On Raspberry Pi
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus i2c-tools
pip3 install -r requirements.txt
sudo raspi-config  # Enable I2C
```

### 2. Connect Hardware
- Follow `hardware/hardware_setup.md`
- Test: `python3 hardware/ev_navigation_hardware.py`

### 3. Run Demo
```bash
cd hardware_demo/demo
python3 run_hardware_demo.py
```

That's it! The script automatically starts:
- ✅ FL Server
- ✅ Hardware Client (with torch running on Pi)
- ✅ 3 Software Clients

## 🔧 Distributed Setup (Server on Different Machine)

### On Server Machine:
```bash
pip3 install torch numpy
cd hardware_demo/demo
python3 server.py
```

### On Raspberry Pi:
```bash
pip3 install -r requirements.txt  # torch + hardware libs
cd hardware_demo/demo
python3 hardware_fl_client.py --id vehicle_00 --host <server-ip>
```

## 📦 What's in requirements.txt?

- **torch>=1.12.0** - For federated learning (runs on Pi!)
- **numpy>=1.21.0** - Numerical operations
- **RPi.GPIO>=0.7.0** - GPIO control (Pi only)
- **adafruit-circuitpython-ssd1306>=2.12.0** - OLED display (Pi only)
- **Pillow>=9.0.0** - Image processing for OLED (Pi only)
- **adafruit-blinka>=8.0.0** - I2C communication (Pi only)

## 🎮 What You'll See

1. **OLED Display**: Real-time FL status
   - Round number
   - Current accuracy
   - Selection status

2. **Servo Motor**: Moves when client is selected

3. **Keypad Controls**:
   - `1`: FL Status
   - `2`: Navigation Demo
   - `3`: Privacy Info
   - `4`: Training Statistics
   - `5`: Client Information
   - `6`: Help Menu
   - `7`: Cycle Stations
   - `8`: Model Performance
   - `0`: Refresh Display
   - `*`: Toggle Mode
   - `#`: Exit

## ❓ Common Questions

**Q: Can I run without hardware?**  
A: Yes! It will use mock mode (no physical hardware needed).

**Q: Does torch work on Raspberry Pi?**  
A: Yes! PyTorch supports ARM architecture. Install with `pip3 install torch`.

**Q: Can server run on Pi too?**  
A: Yes! Everything can run on the same Pi (recommended for demos).

**Q: What if torch installation fails on Pi?**  
A: Try installing from PyTorch's official ARM builds or use a pre-built wheel.

## 🔍 Troubleshooting

- **Hardware not detected**: Check I2C with `sudo i2cdetect -y 1`
- **Torch import error**: Reinstall with `pip3 install --upgrade torch`
- **Connection issues**: Check firewall, ensure ports 8080-8200 are open

