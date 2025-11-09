# Troubleshooting Guide

## Issue: Server Output Not Showing

### Problem
When running `run_hardware_demo.py`, the server output doesn't appear in the console, even though the server is running.

### Root Cause
This is **NOT** related to hardware connection. The issue is Python's output buffering when stdout is piped through subprocess.

### Solution Applied
The following fixes have been implemented in `run_hardware_demo.py`:

1. **Unbuffered Python execution**: Added `-u` flag to all subprocess calls
   ```python
   [sys.executable, '-u', 'server.py']  # Unbuffered output
   ```

2. **Merged stderr into stdout**: Changed `stderr=subprocess.PIPE` to `stderr=subprocess.STDOUT` to capture all output

3. **Improved output reading**: Changed from iterating over stdout to using `readline()` for better line-by-line reading

4. **Better error detection**: Added checks to detect if server exits unexpectedly

### How to Verify It's Working

1. **Run the demo again**:
   ```bash
   cd hardware_demo/demo
   python3 run_hardware_demo.py
   ```

2. **You should now see**:
   - Server initialization messages
   - "Server listening on localhost:8080"
   - "Waiting for clients to connect..."
   - Client connection messages
   - Round-by-round training progress

3. **If still no output**, try running server directly to check for errors:
   ```bash
   cd hardware_demo/demo
   python3 -u server.py
   ```

### Hardware Connection Status

**Important**: The server output issue is **NOT** related to hardware connection. The server will run and show output regardless of whether:
- OLED display is connected
- Servo motor is connected  
- Keypad is connected

The hardware client will automatically use "mock mode" if hardware is not detected, but the server will still function normally.

### Other Common Issues

#### Server Exits Immediately
- Check if port 8080 is already in use: `lsof -i :8080` or `netstat -an | grep 8080`
- Check for import errors by running server directly: `python3 server.py`

#### Clients Can't Connect
- Ensure server starts before clients
- Check firewall settings
- Verify network connectivity if using distributed setup

#### No Training Happening
- Server waits 10 seconds for clients to connect
- Ensure at least 4 clients connect (check client connection messages)
- Check that clients are actually training (look for "Training..." messages)

### Debug Mode

To see all output in real-time, you can run components separately:

**Terminal 1 - Server:**
```bash
cd hardware_demo/demo
python3 -u server.py
```

**Terminal 2 - Hardware Client:**
```bash
cd hardware_demo/demo
python3 -u hardware_fl_client.py --id vehicle_00
```

**Terminal 3 - Software Clients:**
```bash
cd hardware_demo/demo
python3 -u client.py --id vehicle_01
```

This way you'll see all output directly without any buffering issues.

