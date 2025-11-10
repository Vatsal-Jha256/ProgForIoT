# FedRoute Hardware Demo

A **standalone** hardware demonstration of the FedRoute federated learning system for Internet of Vehicles (IoV). This demo showcases the system's capabilities using physical hardware components: OLED display, servo motor, and keypad.

**⚠️ IMPORTANT: This demo is completely independent** - it does not require or import anything from the parent FedRoute repository. It's designed to run standalone for presentations and demonstrations.

## 🎯 Overview

This hardware demo provides an interactive demonstration of FedRoute's key features:

1. **Federated Learning Demo**: Complete FL workflow with visual feedback
2. **POI & Navigation Demo**: NYC-specific POI recommendations with music suggestions
3. **System Information**: Model architecture and privacy features

**Features:**
- ✅ Completely standalone - no parent repo dependencies
- ✅ Fast and simple - perfect for presentations
- ✅ NYC-specific POI and music data
- ✅ Simulation mode for testing without hardware

## 🔧 Hardware Requirements

### Components
- Raspberry Pi (any model with GPIO pins)
- OLED Display (SSD1306, 128x64)
- Servo Motor (SG90 or similar)
- 4x4 Matrix Keypad

### Connections

See `hardware_setup.md` for detailed connection instructions.

**Quick Reference:**
- **OLED**: I2C (SDA: Pin 3, SCL: Pin 5)
- **Servo**: GPIO 18 (Pin 12)
- **Keypad**: 
  - Rows: GPIO 23, 24, 25, 8
  - Cols: GPIO 7, 12, 16, 20

**Note**: The 'A' key on the keypad does not work. Use keys 1-9, 0, B, C, #, *.

## 📦 Software Setup

### 1. Install Dependencies

```bash
# System packages (Raspberry Pi only)
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus i2c-tools

# Python packages (standalone - no parent repo needed)
cd hardware_demo
pip3 install -r requirements.txt

# For simulation mode (no hardware), only numpy is needed:
pip3 install numpy
```

### 2. Enable I2C

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
```

### 3. Verify Hardware

```bash
# Check I2C devices
sudo i2cdetect -y 1
# Should show OLED at address 0x3C
```

## 🚀 Running the Demo

### On Raspberry Pi (Hardware Mode)

**📖 For detailed setup instructions, see [SETUP_RASPBERRY_PI.md](SETUP_RASPBERRY_PI.md)**

Quick start:
```bash
cd hardware_demo

# Install dependencies
pip3 install -r requirements.txt

# Run the demo (NO --simulation flag!)
python3 main_demo.py
```

**Important:** Do NOT use `--simulation` flag when running on actual hardware!

### On Development Machine (Simulation Mode)

```bash
cd hardware_demo
python3 main_demo.py --simulation
```

In simulation mode, the demo runs without hardware and uses console input/output instead.

## 🎮 Using the Demo

### Main Menu

The demo starts with an interactive menu:

```
Main Menu

4. Federated Learning Demo
5. POI & Navigation Demo
6. System Information

* = Exit
```

**Note**: Use keys 4, 5, 6 (keys 1, 2, 3, A don't work on this keypad).

### Navigation

- **Keys 4-6**: Select menu option (1, 2, 3, A don't work)
- **Key ***: Exit demo
- **Other keys**: Invalid (ignored)

**Note**: Keys 1, 2, 3, and A do not work on the keypad. Use 4, 5, 6 instead.

### Demo Options

#### Option 1: Federated Learning Demo

Demonstrates the complete federated learning workflow:

1. **Initialization**: Model setup and client connection
2. **Client Selection**: Multi-objective selection of participants
3. **Model Broadcast**: Global model distribution
4. **Local Training**: Privacy-preserving on-device training
5. **Aggregation**: Secure aggregation with differential privacy
6. **Results**: Accuracy metrics and privacy summary

**Duration**: ~2-3 minutes

#### Option 2: POI & Navigation Demo

Shows intelligent POI recommendations and music suggestions using **NYC-specific data**:

1. **Context Analysis**: Current location (NYC Manhattan) and conditions
2. **POI Discovery**: FL model-based POI recommendations (NYC landmarks)
3. **POI Selection**: Interactive selection (keys 1-3)
4. **Navigation**: Simulated route guidance to selected POI
5. **Music Recommendations**: NYC-style music suggestions based on POI category
6. **Journey Summary**: Complete trip overview

**NYC POIs include**: Central Park, Times Square, Empire State Building, Broadway Theater, MoMA, JFK Airport, Coney Island, and more!

**Duration**: ~2-3 minutes

#### Option 3: System Information

Displays system architecture and features:

1. **Model Information**: Parameters and architecture
2. **Privacy Features**: Differential privacy guarantees
3. **System Architecture**: Client-server FL structure
4. **Key Features**: FedRoute capabilities

**Duration**: ~1-2 minutes

## 🎨 Visual Feedback

### OLED Display
- Shows menus, status messages, and results
- Updates in real-time during demos
- Supports multi-line text

### Servo Motor
- **Menu Navigation**: Subtle movements
- **Processing**: Animated during operations
- **Success**: Celebration animations
- **Progress**: Visual feedback during long operations

### Keypad
- Real-time key press detection
- Debounced input (200ms)
- Visual feedback on OLED

## 📁 File Structure

```
hardware_demo/
├── main_demo.py              # Main interactive menu system
├── hardware_controller.py    # Hardware abstraction layer
├── demo_federated_learning.py  # Option 1: FL demo
├── demo_poi_navigation.py    # Option 2: POI & navigation demo
├── demo_system_info.py       # Option 3: System information
├── hardware_setup.md         # Hardware connection guide
└── README.md                 # This file
```

## 🔍 Features Demonstrated

### Privacy-Preserving Federated Learning
- ✅ Local data training (data never leaves device)
- ✅ Differential privacy (ε-DP with noise injection)
- ✅ Secure aggregation
- ✅ Client selection based on context similarity

### Intelligent Recommendations
- ✅ POI recommendations using FL model
- ✅ Context-aware music suggestions
- ✅ Real-time inference
- ✅ Multi-task learning (POI + Music)

### System Architecture
- ✅ FMTL model structure
- ✅ Privacy guarantees
- ✅ Federated learning workflow
- ✅ IoV-specific optimizations

## 🐛 Troubleshooting

### OLED Display Not Working

```bash
# Check I2C connection
sudo i2cdetect -y 1

# Verify I2C is enabled
sudo raspi-config

# Check wiring (SDA: Pin 3, SCL: Pin 5)
```

### Servo Not Moving

```bash
# Check power supply (needs 5V)
# Verify GPIO 18 connection
# Test with: python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(18, GPIO.OUT); pwm = GPIO.PWM(18, 50); pwm.start(7.5)"
```

### Keypad Not Responding

```bash
# Check all row/column connections
# Verify pull-up resistors
# Test individual keys
```

### Import Errors

```bash
# Install missing packages
pip3 install RPi.GPIO adafruit-circuitpython-ssd1306 pillow

# For simulation mode, no hardware packages needed
python3 main_demo.py --simulation
```

## 🎓 Educational Value

This demo is designed to:

1. **Visualize FL Concepts**: See federated learning in action
2. **Demonstrate Privacy**: Show how data stays local
3. **Showcase IoV Applications**: Real-world use cases
4. **Interactive Learning**: Hands-on exploration

Perfect for:
- Research presentations
- Educational demonstrations
- System validation
- Proof of concept

## 📝 Notes

- **Standalone**: This demo is completely independent - no parent repo needed
- **Fast & Simple**: Designed for quick presentations, not full system simulation
- **NYC Data**: Uses NYC-specific POIs and music recommendations
- **Mock Models**: Uses simplified mock models for demonstration (no actual model loading)
- **Presentation Focus**: Optimized for convincing demonstrations to teachers/audiences
- All privacy mechanisms are demonstrated conceptually

## 🤝 Contributing

To extend the demo:

1. Add new demo modules in `demo_*.py` files
2. Register in `main_demo.py` menu
3. Use `HardwareController` for hardware access
4. Follow existing demo patterns

## 📄 License

See main project LICENSE file.

## 🙏 Acknowledgments

- FedRoute research team
- Hardware setup based on `hardware_setup.md`
- Uses Adafruit CircuitPython libraries for OLED

---

**For questions or issues, please refer to the main project README or open an issue.**
