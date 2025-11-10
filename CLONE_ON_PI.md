# Clone and Setup on Raspberry Pi

Quick commands to clone and set up the FedRoute hardware demo on your Raspberry Pi.

## 🚀 Quick Setup Commands

### 1. Clone the Repository

```bash
cd ~
git clone git@github.com:Vatsal-Jha256/ProgForIoT.git
cd ProgForIoT
```

**Or if you don't have SSH keys set up:**

```bash
cd ~
cd ProgForIoT
```

### 2. Install Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-smbus i2c-tools

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 3. Enable I2C (if not already enabled)

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
sudo reboot
```

### 4. Verify Hardware

```bash
# Check OLED is detected
sudo i2cdetect -y 1
# Should show "3C" for OLED display
```

### 5. Run the Demo

```bash
# Make sure you're in the repo directory
cd ~/ProgForIoT

# Activate venv if you created one
source venv/bin/activate

# Run the demo (NO --simulation flag!)
python3 main_demo.py
```

## 📋 Complete One-Line Setup (After Hardware is Connected)

```bash
cd ~ && git clone git@github.com:Vatsal-Jha256/ProgForIoT.git && cd ProgForIoT && sudo apt-get update && sudo apt-get install -y python3-pip python3-venv python3-smbus i2c-tools && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && echo "✅ Setup complete! Run: python3 main_demo.py"
```

## 🔑 Keypad Controls

- **Keys 4, 5, 6**: Select menu options (keys 1, 2, 3, A don't work)
- **Key ***: Exit demo

## 📖 For Detailed Instructions

See `SETUP_RASPBERRY_PI.md` for complete setup guide with troubleshooting.

