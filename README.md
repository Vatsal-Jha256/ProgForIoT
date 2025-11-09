# FedRoute Hardware Demo

This directory contains a standalone hardware demonstration of the FedRoute federated learning system, designed to run on Raspberry Pi with physical hardware components.

## Overview

The hardware demo showcases:
- **Privacy-preserving federated learning** on physical hardware
- **Real-time status display** on OLED screen
- **Client selection visualization** using servo motor
- **Interactive controls** via keypad
- **Navigation recommendations** using FL model

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- OLED Display (SSD1306, 128x64, I2C)
- Servo Motor (SG90 or similar)
- 4x4 Matrix Keypad

See `hardware/hardware_setup.md` for detailed connection instructions.

## Software Requirements

### For Hardware Controller Only (Standalone):
If you only need the hardware controller (`hardware/ev_navigation_hardware.py`):
```bash
# Install hardware-only dependencies
pip3 install -r requirements-hardware.txt
```

### For Full Demo (FL + Hardware):
**On Raspberry Pi (Hardware Client):**
```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus i2c-tools

# Install ALL dependencies (torch, numpy, + hardware libraries)
pip3 install -r requirements.txt

# Enable I2C
sudo raspi-config
# Select Interface Options > I2C > Enable
```

**Note:** `requirements.txt` includes both torch/numpy (for FL) AND hardware libraries. 
The hardware client runs torch on Raspberry Pi to train models locally.

### On Non-Raspberry Pi Systems:
The demo will run in mock mode (no hardware required):
```bash
# For full demo (FL + mock hardware)
pip3 install torch numpy

# For hardware controller only (mock mode)
# No additional packages needed - uses standard library only
```

## Directory Structure

```
hardware_demo/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── demo/                     # Demo scripts
│   ├── run_hardware_demo.py  # Main launcher
│   ├── hardware_fl_client.py # Hardware FL client
│   ├── server.py             # FL server
│   └── client.py             # Software FL client
├── hardware/                 # Hardware control
│   ├── ev_navigation_hardware.py
│   └── hardware_setup.md
├── navigation/               # Routing algorithms
│   └── ev_routing_algorithm.py
└── src/                      # Model definitions
    └── models/
        └── fmtl_model.py
```

## Architecture: What Runs Where?

### Components Overview

1. **FL Server** (`demo/server.py`)
   - Runs on: **Any machine** (can be Raspberry Pi or separate computer)
   - Needs: `torch`, `numpy`
   - Purpose: Coordinates federated learning, aggregates model updates

2. **Hardware FL Client** (`demo/hardware_fl_client.py`)
   - Runs on: **Raspberry Pi** (with physical hardware connected)
   - Needs: `torch`, `numpy` + hardware libraries (`RPi.GPIO`, `adafruit-ssd1306`, etc.)
   - Purpose: Participates in FL, displays status on OLED, controls servo/keypad
   - **YES, torch runs on Raspberry Pi** - the client trains models locally using torch

3. **Software FL Clients** (`demo/client.py`)
   - Runs on: **Any machine** (optional, for comparison)
   - Needs: `torch`, `numpy`
   - Purpose: Additional clients to demonstrate multi-client FL

### Typical Setup Options

**Option 1: Everything on Raspberry Pi** (Recommended for demo)
- Server + Hardware Client + Software Clients all on same Pi
- Simple setup, good for demonstrations

**Option 2: Distributed Setup**
- Server on separate machine (laptop/desktop)
- Hardware Client on Raspberry Pi
- Software Clients on any machines
- More realistic distributed FL scenario

## Quick Start

### Step 1: Install Dependencies

**On Raspberry Pi (for Hardware Client):**
```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus i2c-tools

# Install all dependencies (torch + hardware libraries)
pip3 install -r requirements.txt

# Enable I2C interface
sudo raspi-config
# Select: Interface Options > I2C > Enable
```

**On Server Machine (if different from Pi):**
```bash
# Install only FL dependencies
pip3 install torch numpy
```

### Step 2: Setup Hardware (Raspberry Pi only)
- Follow instructions in `hardware/hardware_setup.md`
- Verify connections:
  ```bash
  cd hardware_demo/hardware
  python3 ev_navigation_hardware.py
  ```

### Step 3: Run the Demo

**Option A: All-in-One (Everything on Raspberry Pi)**
```bash
cd hardware_demo/demo
python3 run_hardware_demo.py
```
This automatically starts:
- FL Server
- Hardware FL Client (with OLED, Servo, Keypad)
- 3 additional software clients

**Option B: Manual Setup (Distributed)**

Terminal 1 - Start Server:
```bash
cd hardware_demo/demo
python3 server.py
```

Terminal 2 - Start Hardware Client (on Raspberry Pi):
```bash
cd hardware_demo/demo
python3 hardware_fl_client.py --id vehicle_00 --host <server-ip>
```

Terminal 3+ - Start Software Clients (optional):
```bash
cd hardware_demo/demo
python3 client.py --id vehicle_01 --host <server-ip>
python3 client.py --id vehicle_02 --host <server-ip>
```

### Step 4: Watch the Hardware
- **OLED Display**: Shows FL status in real-time (round, accuracy, selection)
- **Servo Motor**: Moves when client is selected for training
- **Keypad**: Interactive controls (see Keypad Controls below)

## Keypad Controls

- **1**: Show FL Status (round, accuracy, selection)
- **2**: Demo Navigation (using FL model recommendations)
- **3**: Show Privacy Information
- **#**: Exit client

## Features Demonstrated

### Privacy-Preserving Learning
- All training data stays on-device
- Only model updates (not raw data) are sent to server
- Demonstrates federated learning principles

### Real-Time Visualization
- **OLED Display**: Shows current FL round, accuracy, and selection status
- **Servo Motor**: Visual indicator when client is selected for training
- **Keypad**: Interactive controls for exploring features

### Navigation Integration
- Uses FL model to recommend charging stations
- Demonstrates practical application of federated learning
- Shows how FL improves recommendations over time

## How It Works

1. **Server** coordinates federated learning across multiple clients
2. **Hardware Client** connects and displays status on OLED
3. **Server selects clients** for each round (including hardware client)
4. **Selected clients train locally** on private data (data never leaves device)
5. **Model updates** are sent back to server
6. **Server aggregates** updates using FedAvg
7. **Process repeats** for multiple rounds

## Troubleshooting

### Hardware Not Detected
- Check I2C connection: `sudo i2cdetect -y 1`
- Verify GPIO connections
- Ensure hardware libraries are installed

### Mock Mode
- If not on Raspberry Pi, the system automatically uses mock hardware
- All functionality works, but no physical hardware is used
- Perfect for testing on development machines

### Connection Issues
- Ensure server starts before clients
- Check firewall settings
- Verify ports 8080-8200 are available

## License

Part of the FedRoute project. See main project README for license information.

## Support

For issues or questions:
1. Check `hardware/hardware_setup.md` for hardware troubleshooting
2. Review demo output for error messages
3. Ensure all dependencies are installed correctly


