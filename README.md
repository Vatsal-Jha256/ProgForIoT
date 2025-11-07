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

### On Raspberry Pi:
```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus i2c-tools

# Install Python packages
pip3 install torch numpy
pip3 install RPi.GPIO adafruit-circuitpython-ssd1306 Pillow adafruit-blinka

# Enable I2C
sudo raspi-config
# Select Interface Options > I2C > Enable
```

### On Non-Raspberry Pi Systems:
The demo will run in mock mode (no hardware required):
```bash
pip3 install torch numpy
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

## Quick Start

1. **Setup Hardware** (Raspberry Pi only):
   - Follow instructions in `hardware/hardware_setup.md`
   - Verify connections with `python3 hardware/ev_navigation_hardware.py`

2. **Run the Demo**:
   ```bash
   cd hardware_demo/demo
   python3 run_hardware_demo.py
   ```

3. **Watch the Hardware**:
   - OLED display shows FL status in real-time
   - Servo motor moves when client is selected
   - Use keypad for interactive controls

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

