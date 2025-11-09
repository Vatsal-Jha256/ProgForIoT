#!/usr/bin/env python3
"""
FedRoute Hardware Demo Launcher
Demonstrates federated learning on physical hardware

Launches:
1. FL Server (coordinates federated learning)
2. Hardware FL Client (with OLED, Servo, Keypad)
3. Optional: Additional software clients for comparison

This demo showcases:
- Privacy-preserving federated learning
- Real-time hardware status display
- Client selection visualization
- Navigation recommendations using FL model

Author: FedRoute Team
Date: October 2025
"""

import subprocess
import time
import sys
import os
from pathlib import Path
import threading
import queue
import re

# Change to demo directory
demo_dir = Path(__file__).parent
os.chdir(demo_dir)

print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        🚗 FEDROUTE HARDWARE DEMO - PHYSICAL FL DEMONSTRATION 🚗   ║
║                                                                    ║
║  Privacy-Preserving Federated Learning on Physical Hardware       ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

This demo will launch:
  🌐 FL Server: Coordinating federated learning
  🚗 Hardware Client: Physical hardware with OLED, Servo, Keypad
  📱 Software Clients: Additional clients for comparison (optional)

Hardware Features Demonstrated:
  ✓ OLED Display: Real-time FL status (round, accuracy, selection)
  ✓ Servo Motor: Visual indicator when client is selected
  ✓ Keypad: Interactive controls for demo navigation
  ✓ Privacy: All training data stays on-device

Core Principles Shown:
  ✓ Privacy-Preserving: Data never leaves the vehicle
  ✓ Federated Learning: Collaborative model training
  ✓ Client Selection: Multi-objective selection algorithm
  ✓ Real-time Updates: Live status on hardware display

""")

input("Press Enter to start the hardware demo...")

processes = []

def parse_server_output(line, output_queue):
    """Parse server output and display relevant information."""
    # Display important server messages
    if "ROUND" in line and not "=" in line:
        match = re.search(r'ROUND (\d+)', line)
        if match:
            print(f"\n{'='*70}")
            print(f"ROUND {match.group(1)} - Hardware client participating...")
            print(f"{'='*70}")
    
    if "Selected clients:" in line:
        match = re.search(r'Selected clients: (.+)', line)
        if match:
            clients = match.group(1).strip().split(', ')
            print(f"🎯 Selected clients: {', '.join(clients)}")
            if any('vehicle_00' in c or 'hardware' in c.lower() for c in clients):
                print("   ✅ Hardware client SELECTED - Watch the servo motor!")
    
    if "Path Accuracy:" in line or "Music Accuracy:" in line or "Combined Accuracy:" in line:
        print(line.strip())

try:
    # 1. Start FL Server
    print("\n[1/2] 🌐 Starting FL Server...")
    server_process = subprocess.Popen(
        [sys.executable, '-u', 'server.py'],  # -u flag for unbuffered output
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        text=True,
        bufsize=1
    )
    processes.append(('Server', server_process))
    time.sleep(3)  # Give server time to initialize and print startup messages
    print("   ✅ Server started")
    
    # Check if server is still running
    if server_process.poll() is not None:
        print("   ❌ Server process exited immediately!")
        print("   Check for errors above or run server.py directly to debug")
        sys.exit(1)
    
    # 2. Start Hardware FL Client
    print("\n[2/2] 🚗 Starting Hardware FL Client...")
    print("   Make sure your hardware is connected!")
    print("   - OLED Display (SSD1306) on I2C")
    print("   - Servo Motor on GPIO 18")
    print("   - Keypad connected to GPIO pins")
    print()
    
    hardware_client_process = subprocess.Popen(
        [sys.executable, '-u', 'hardware_fl_client.py', '--id', 'vehicle_00'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    processes.append(('Hardware Client', hardware_client_process))
    time.sleep(4)  # Give hardware client more time to initialize and bind socket
    print("   ✅ Hardware client started")
    
    # Optional: Start additional software clients for comparison
    print("\n[Optional] Starting additional software clients...")
    num_software_clients = 3
    
    for i in range(1, num_software_clients + 1):
        client_id = f"vehicle_{i:02d}"
        client_process = subprocess.Popen(
            [sys.executable, '-u', 'client.py', '--id', client_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append((client_id, client_process))
        time.sleep(1)  # Give each client time to bind their socket
    
    print(f"   ✅ {num_software_clients} additional clients started\n")
    
    print("="*70)
    print("🎉 HARDWARE DEMO RUNNING!")
    print("="*70)
    print("""
Watch your hardware:
  📺 OLED Display: Shows FL status in real-time
     - Round number
     - Current accuracy
     - Selection status (Selected ✓ / Waiting...)
  
  🎚️  Servo Motor: Moves when client is selected
     - RIGHT position = Selected for training
     - STRAIGHT position = Waiting
  
  ⌨️  Keypad Controls:
     1: Show FL Status
     2: Demo Navigation (using FL model recommendations)
     3: Show Privacy Information
     #: Exit client

The server will:
  1. Select clients for each round (including hardware client)
  2. Send global model to selected clients
  3. Clients train locally (PRIVACY: data stays on-device)
  4. Receive model updates
  5. Aggregate and update global model
  6. Repeat for 15 rounds

""")
    
    print("📊 Server Output:")
    print("-" * 70)
    sys.stdout.flush()
    
    # Monitor server output
    output_queue = queue.Queue()
    
    def read_server_output():
        """Read server output in background thread."""
        try:
            for line in iter(server_process.stdout.readline, ''):
                if not line:
                    break
                output_queue.put(line)
                if "TRAINING COMPLETE" in line:
                    break
        except Exception as e:
            print(f"Error reading server output: {e}")
    
    reader_thread = threading.Thread(target=read_server_output, daemon=True)
    reader_thread.start()
    
    training_complete = False
    no_output_count = 0
    
    try:
        while not training_complete:
            # Process server output from queue
            try:
                line = output_queue.get(timeout=0.5)
                print(line, end='', flush=True)
                parse_server_output(line, output_queue)
                no_output_count = 0  # Reset counter when we get output
                
                if "TRAINING COMPLETE" in line:
                    print("\n✅ All rounds completed successfully!")
                    training_complete = True
            except queue.Empty:
                no_output_count += 1
                # Check if server is still running
                if server_process.poll() is not None:
                    if no_output_count > 2:
                        print("\n⚠️  Server process ended unexpectedly")
                        # Try to read any remaining output
                        try:
                            remaining = server_process.stdout.read()
                            if remaining:
                                print(remaining)
                        except:
                            pass
                        training_complete = True
                        break
                elif no_output_count == 10:
                    # Give a status update if no output for 5 seconds
                    print("⏳ Waiting for server output... (server is running)")
                    no_output_count = 0
                
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    
    print("\n" + "="*70)
    print("✅ Hardware Demo Complete!")
    print("="*70)
    print("""
Summary:
  ✓ Hardware client participated in federated learning
  ✓ Real-time status displayed on OLED
  ✓ Servo motor indicated selection status
  ✓ Privacy preserved (data never left the device)
  ✓ Navigation recommendations using FL model
  ✓ Interactive keypad controls demonstrated

Thank you for trying FedRoute Hardware Demo!
""")
    
except KeyboardInterrupt:
    print("\n\n⚠️  Demo interrupted by user")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Cleanup
    print("\n🧹 Cleaning up...")
    for name, process in processes:
        try:
            process.terminate()
            process.wait(timeout=2)
            print(f"   ✓ Stopped {name}")
        except:
            try:
                process.kill()
            except:
                pass
    
    print("\n👋 Goodbye!\n")


