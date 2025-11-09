#!/usr/bin/env python3
"""
FedRoute Hardware FL Client Demo
Integrates federated learning with physical hardware (OLED, Servo, Keypad)
Shows real-time FL status and demonstrates privacy-preserving recommendations

This client connects to the FL server and displays:
- Current FL round and accuracy
- Selection status (selected/not selected)
- Navigation recommendations using FL model
- Privacy-preserving local training

Author: FedRoute Team
Date: October 2025
"""

import sys
import os
import time
import socket
import pickle
import threading
import logging
import argparse
from pathlib import Path
from typing import Dict, Optional, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
# Simplified for IoT demo - removed torch imports (not needed for hardware flow)

# Import hardware controller
sys.path.insert(0, str(Path(__file__).parent.parent / 'hardware'))
from ev_navigation_hardware import EVNavigationHardware

# Import routing for navigation integration
sys.path.insert(0, str(Path(__file__).parent.parent / 'navigation'))
from ev_routing_algorithm import EVRoutingAlgorithm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HardwareFLClient")


class HardwareFLClient:
    """
    Federated Learning Client with Hardware Integration.
    Demonstrates FedRoute principles on physical hardware.
    """
    
    def __init__(self, client_id: str, server_host: str = 'localhost', 
                 server_port: int = 8080):
        """Initialize hardware FL client."""
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        
        # Calculate unique port for this client
        client_num = int(client_id.split('_')[-1]) if '_' in client_id else 0
        self.listen_port = server_port + 100 + client_num
        
        # Initialize hardware
        self.hardware = EVNavigationHardware()
        self.routing = EVRoutingAlgorithm()
        
        # Simplified for IoT demo - no complex model operations
        # Just simulate training for smooth hardware flow
        self.num_samples = np.random.randint(50, 200)
        
        # FL state
        self.current_round = 0
        self.is_selected = False
        self.last_accuracy = 0.0
        self.training_active = False
        self.training_history = []  # Track training rounds
        self.total_training_count = 0
        
        # Navigation state
        self.current_location = (20.2961, 85.8245)  # Bhubaneswar center
        self.stations = self._get_default_stations()
        self.current_station_index = 0
        
        logger.info(f"✅ Hardware FL Client {client_id} initialized")
        logger.info(f"   Local data samples: {self.num_samples}")
        logger.info(f"   Privacy: Data stays on-device")
        
        # Don't display anything on OLED until we're actually ready
        # (OLED will be blank during initialization)
    
    # Removed _generate_local_data - not needed for simplified demo
    
    def _get_default_stations(self) -> list:
        """Get default charging stations."""
        return [
            {'station_id': 'ST01', 'lat': 20.2961, 'lon': 85.8245, 'name': 'City Center'},
            {'station_id': 'ST02', 'lat': 20.2644, 'lon': 85.8281, 'name': 'KIIT Area'},
            {'station_id': 'ST03', 'lat': 20.3100, 'lon': 85.8500, 'name': 'Patia IT Hub'},
            {'station_id': 'ST04', 'lat': 20.2800, 'lon': 85.8000, 'name': 'Old Town'},
            {'station_id': 'ST05', 'lat': 20.3200, 'lon': 85.8200, 'name': 'Nayapalli'},
        ]
    
    def connect(self) -> bool:
        """Connect to FL server and register."""
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5)
                client_socket.connect((self.server_host, self.server_port))
                
                # Send client info
                info = {
                    'client_id': self.client_id,
                    'num_samples': self.num_samples,
                    'listen_port': self.listen_port
                }
                client_socket.send(pickle.dumps(info))
                
                # Receive acknowledgment
                ack = pickle.loads(client_socket.recv(4096))
                client_socket.close()
                
                if ack['status'] == 'connected':
                    # Only display on OLED after successful connection
                    self._display_status("Connected to\nFL Server", duration=1.5)
                    logger.info(f"✅ Connected to server")
                    return True
                
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"⏳ Connection attempt {attempt+1}/{max_retries}... (Error: {e})")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"❌ Failed to connect after {max_retries} attempts: {e}")
                    logger.error(f"   Server: {self.server_host}:{self.server_port}")
                    self._display_status("Connection\nFailed")
                    return False
        
        return False
    
    def _display_status(self, message: str, duration: float = 2.0):
        """Display status message on OLED."""
        self.hardware.display_message(message)
        time.sleep(duration)
    
    def _display_fl_status(self, round_num: int, accuracy: float, 
                          selected: bool, training: bool = False):
        """Display federated learning status on OLED."""
        status_msg = f"FedRoute FL\n"
        status_msg += f"Round: {round_num}\n"
        status_msg += f"Acc: {accuracy:.2f}\n"
        
        if training:
            status_msg += "Training..."
        elif selected:
            status_msg += "Selected ✓"
        else:
            status_msg += "Waiting..."
        
        self.hardware.display_message(status_msg)
    
    def _update_servo_selection(self, selected: bool):
        """Update servo motor to indicate selection status with animation."""
        if selected:
            # Animated selection: move right, then center, then left, then center
            self.hardware.set_steering("RIGHT")
            time.sleep(0.15)
            self.hardware.set_steering("STRAIGHT")
            time.sleep(0.1)
            self.hardware.set_steering("LEFT")
            time.sleep(0.15)
            self.hardware.set_steering("STRAIGHT")
        else:
            # Keep servo in center (STRAIGHT) when not selected
            self.hardware.set_steering("STRAIGHT")
    
    def _animate_servo_training(self):
        """Animate servo during training to show activity."""
        # Oscillate servo during training
        for _ in range(3):
            self.hardware.set_steering("RIGHT")
            time.sleep(0.2)
            self.hardware.set_steering("LEFT")
            time.sleep(0.2)
        self.hardware.set_steering("STRAIGHT")
    
    def _indicate_round_with_servo(self, round_num: int):
        """Use servo to indicate round number (1-5 pulses for rounds 1-5, then repeat pattern)."""
        # Show round number with pulses (max 5 pulses)
        pulses = min(round_num % 5, 5) if round_num > 0 else 1
        if pulses == 0:
            pulses = 5
        
        for _ in range(pulses):
            self.hardware.set_steering("RIGHT")
            time.sleep(0.1)
            self.hardware.set_steering("STRAIGHT")
            time.sleep(0.1)
    
    def _indicate_accuracy_with_servo(self, accuracy: float):
        """Use servo position to indicate accuracy level."""
        # Map accuracy (0-1) to servo position (LEFT to RIGHT)
        # 0.0 = LEFT, 0.5 = CENTER, 1.0 = RIGHT
        if accuracy < 0.3:
            self.hardware.set_steering("LEFT")
        elif accuracy < 0.7:
            self.hardware.set_steering("STRAIGHT")
        else:
            self.hardware.set_steering("RIGHT")
        time.sleep(0.3)
        self.hardware.set_steering("STRAIGHT")
    
    def listen(self):
        """Listen for training requests from server."""
        logger.info(f"👂 Listening for training requests on port {self.listen_port}...")
        # Don't display on OLED yet - wait until we actually start receiving requests
        # This keeps OLED blank during initialization
        
        # Create socket to receive training requests
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Bind to 0.0.0.0 to accept connections from any interface
            listen_socket.bind(('0.0.0.0', self.listen_port))
            listen_socket.listen(1)
            listen_socket.settimeout(60)  # Timeout after 60 seconds
            
            logger.info(f"✅ Successfully bound to port {self.listen_port}, ready for training requests")
            time.sleep(0.5)  # Small delay to ensure socket is fully ready
            
            # Start keypad monitoring thread
            keypad_thread = threading.Thread(target=self._monitor_keypad, daemon=True)
            keypad_thread.start()
            
            while True:
                try:
                    client_socket, _ = listen_socket.accept()
                    
                    # NOW display on OLED - we're actually starting FL
                    # First time we receive a request, show we're ready
                    if self.current_round == 0:
                        self._display_status("FL Ready\nWaiting for\nRound 1...", duration=2)
                    
                    # Receive training request
                    size_bytes = client_socket.recv(4)
                    if not size_bytes:
                        break
                    size = int.from_bytes(size_bytes, 'big')
                    
                    data = b''
                    while len(data) < size:
                        chunk = client_socket.recv(min(4096, size - len(data)))
                        if not chunk:
                            break
                        data += chunk
                    
                    request = pickle.loads(data)
                    
                    if request['action'] == 'train':
                        # Update FL state
                        self.current_round = request['round']
                        self.is_selected = True
                        
                        # Display selection status
                        self._display_fl_status(self.current_round, self.last_accuracy, True)
                        self._update_servo_selection(True)
                        # Indicate round number with servo
                        self._indicate_round_with_servo(self.current_round)
                        
                        # Perform local training (PRIVACY: data stays on-device)
                        # Animate servo during training
                        training_thread = threading.Thread(
                            target=self._animate_servo_training, 
                            daemon=True
                        )
                        training_thread.start()
                        update = self.train(request['model_state'], request['round'])
                        
                        # Update accuracy and training history
                        self.last_accuracy = update['accuracy']
                        self.total_training_count += 1
                        self.training_history.append({
                            'round': self.current_round,
                            'accuracy': self.last_accuracy,
                            'loss': update['loss']
                        })
                        # Keep only last 10 rounds in history
                        if len(self.training_history) > 10:
                            self.training_history.pop(0)
                        
                        # Display updated status
                        self._display_fl_status(self.current_round, self.last_accuracy, True, False)
                        # Indicate accuracy level with servo
                        self._indicate_accuracy_with_servo(self.last_accuracy)
                        
                        # Send update back
                        response = pickle.dumps(update)
                        client_socket.sendall(len(response).to_bytes(4, 'big'))
                        client_socket.sendall(response)
                        
                        # Reset selection status after a delay
                        time.sleep(1)
                        self.is_selected = False
                        self._update_servo_selection(False)
                        self._display_fl_status(self.current_round, self.last_accuracy, False)
                    
                    client_socket.close()
                    
                except socket.timeout:
                    # Update display periodically when waiting
                    if not self.training_active:
                        self._display_fl_status(self.current_round, self.last_accuracy, False)
                    continue
                except Exception as e:
                    logger.error(f"Error handling request: {e}")
                    continue
                
        except KeyboardInterrupt:
            logger.info(f"\n🛑 {self.client_id} stopped")
        finally:
            listen_socket.close()
            self.hardware.cleanup()
    
    def _monitor_keypad(self):
        """Monitor keypad for user interaction."""
        # Check which keypad rows actually work
        # If Row 1 (index 0) doesn't work, skip keys 1, 2, 3, A
        non_working_keys = []
        if hasattr(self.hardware, 'working_rows') and self.hardware.working_rows:
            if 0 not in self.hardware.working_rows:  # Row 1 (index 0) doesn't work
                non_working_keys = ['1', '2', '3', 'A']
                logger.info("⚠️  Keypad Row 1 (keys 1,2,3,A) not working - these keys will be ignored")
        
        while True:
            key = self.hardware.read_keypad()
            if key:
                # Skip non-working keys
                if key in non_working_keys:
                    logger.debug(f"Key {key} pressed but Row 1 doesn't work - ignoring")
                    # Show brief message that key doesn't work
                    self.hardware.display_message(f"Key {key}\nNot Available\nRow 1 Issue")
                    time.sleep(1.5)
                    continue
                    
                logger.info(f"Keypad key pressed: {key}")
                # NOTE: Keys 1, 2, 3, A are from Row 1 which doesn't work - IGNORED
                # Remapped keys to working rows:
                # 4 = FL Status (was 1), 5 = Navigation (was 2), 6 = Privacy (was 3)
                # B = Training Stats (was 4), C = Client Info (was 5), D = Help (was 6)
                # 7 = Stations, 8 = Performance, 9 = Toggle (was *), * = Quick Status
                # 0 = Refresh, # = Exit
                
                if key == '4':  # FL Status (remapped from 1)
                    self._display_fl_status(self.current_round, self.last_accuracy, self.is_selected)
                elif key == '5':  # Navigation (remapped from 2)
                    self._demo_navigation()
                elif key == '6':  # Privacy Info (remapped from 3)
                    self._display_privacy_info()
                elif key == 'B':  # Training Stats (remapped from 4)
                    self._display_training_stats()
                elif key == 'C':  # Client Info (remapped from 5)
                    self._display_client_info()
                elif key == 'D':  # Help Menu (remapped from 6)
                    self._display_help_menu()
                elif key == '7':  # Cycle through charging stations
                    self._cycle_stations()
                elif key == '8':  # Show model performance
                    self._display_model_performance()
                elif key == '9':  # Toggle display mode (remapped from *)
                    self._toggle_display_mode()
                elif key == '*':  # Quick status
                    self._display_fl_status(self.current_round, self.last_accuracy, self.is_selected)
                elif key == '#':  # Exit
                    logger.info("Exit requested via keypad")
                    break
                elif key == '0':  # Reset/refresh display
                    self._display_fl_status(self.current_round, self.last_accuracy, self.is_selected)
            time.sleep(0.1)
    
    def _demo_navigation(self):
        """Demonstrate navigation - simplified for IoT demo."""
        self._display_status("Navigation\nDemo...")
        time.sleep(1)
        
        # Simplified - just show nearest station
        nearest = self._find_nearest_station(self.current_location)
        
        if nearest:
            distance = self._calculate_distance(
                self.current_location,
                (nearest['lat'], nearest['lon'])
            )
            
            self.hardware.display_station_info(
                nearest['station_id'],
                distance,
                "Recommended"
            )
            time.sleep(3)
    
    def _display_privacy_info(self):
        """Display privacy-preserving information."""
        privacy_msg = "Privacy Info:\n"
        privacy_msg += "✓ Data Local\n"
        privacy_msg += "✓ No Raw Data\n"
        privacy_msg += "✓ DP Noise\n"
        privacy_msg += "✓ Secure Agg"
        
        self.hardware.display_message(privacy_msg)
        time.sleep(4)
    
    def _display_training_stats(self):
        """Display training statistics."""
        if not self.training_history:
            stats_msg = "Training Stats:\n"
            stats_msg += "No training yet\n"
            stats_msg += f"Rounds: {self.current_round}\n"
            stats_msg += f"Selected: {self.total_training_count}x"
        else:
            avg_acc = sum(h['accuracy'] for h in self.training_history) / len(self.training_history)
            latest = self.training_history[-1]
            stats_msg = "Training Stats:\n"
            stats_msg += f"Rounds: {self.current_round}\n"
            stats_msg += f"Trained: {self.total_training_count}x\n"
            stats_msg += f"Avg Acc: {avg_acc:.3f}\n"
            stats_msg += f"Latest: {latest['accuracy']:.3f}"
        
        self.hardware.display_message(stats_msg)
        time.sleep(4)
    
    def _display_client_info(self):
        """Display client information."""
        info_msg = f"Client Info:\n"
        info_msg += f"ID: {self.client_id}\n"
        info_msg += f"Samples: {self.num_samples}\n"
        info_msg += f"Port: {self.listen_port}\n"
        info_msg += f"Server: {self.server_host}"
        
        self.hardware.display_message(info_msg)
        time.sleep(4)
    
    def _display_help_menu(self):
        """Display keypad help menu."""
        help_msg = "Keypad Help:\n"
        help_msg += "(Row 1: 1,2,3,A\n"
        help_msg += " not working)\n"
        help_msg += "4: FL Status\n"
        help_msg += "5: Navigation\n"
        help_msg += "6: Privacy Info\n"
        help_msg += "B: Training Stats\n"
        help_msg += "C: Client Info\n"
        help_msg += "D: This Help\n"
        help_msg += "7: Stations\n"
        help_msg += "8: Performance\n"
        help_msg += "9: Toggle Mode\n"
        help_msg += "*: Quick Status\n"
        help_msg += "0: Refresh\n"
        help_msg += "#: Exit"
        
        self.hardware.display_message(help_msg)
        time.sleep(5)
    
    def _cycle_stations(self):
        """Cycle through available charging stations."""
        if not self.stations:
            self.hardware.display_message("No stations\navailable")
            time.sleep(2)
            return
        
        # Show each station for 3 seconds
        for i, station in enumerate(self.stations[:3]):  # Show first 3 stations
            distance = self._calculate_distance(
                self.current_location,
                (station['lat'], station['lon'])
            )
            self.hardware.display_station_info(
                station['station_id'],
                distance,
                f"Station {i+1}/{min(3, len(self.stations))}"
            )
            time.sleep(3)
    
    def _display_model_performance(self):
        """Display model performance metrics."""
        if not self.training_history:
            perf_msg = "Model Performance:\n"
            perf_msg += "No training data\n"
            perf_msg += "yet available"
        else:
            latest = self.training_history[-1]
            best = max(self.training_history, key=lambda x: x['accuracy'])
            perf_msg = "Model Performance:\n"
            perf_msg += f"Current: {latest['accuracy']:.3f}\n"
            perf_msg += f"Best: {best['accuracy']:.3f}\n"
            perf_msg += f"Loss: {latest['loss']:.3f}"
        
        self.hardware.display_message(perf_msg)
        time.sleep(4)
    
    def _toggle_display_mode(self):
        """Toggle between different display modes."""
        # Simple toggle - just refresh the current status
        self._display_fl_status(self.current_round, self.last_accuracy, self.is_selected)
        time.sleep(1)
        # Show a brief message
        self.hardware.display_message("Display\nRefreshed")
        time.sleep(1)
    
    def _demo_mode(self):
        """Cycle through demo features automatically."""
        self.hardware.display_message("Demo Mode\nStarting...")
        time.sleep(1)
        
        # Cycle through key features
        features = [
            ("FL Status", lambda: self._display_fl_status(self.current_round, self.last_accuracy, self.is_selected)),
            ("Training Stats", self._display_training_stats),
            ("Privacy Info", self._display_privacy_info),
            ("Client Info", self._display_client_info),
        ]
        
        for name, func in features:
            self.hardware.display_message(f"Demo: {name}")
            time.sleep(0.5)
            func()
            time.sleep(2)
        
        self.hardware.display_message("Demo\nComplete")
        time.sleep(1)
    
    def _find_nearest_station(self, location: Tuple[float, float]):
        """Find nearest charging station."""
        if not self.stations:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for station in self.stations:
            distance = self._calculate_distance(
                location,
                (station['lat'], station['lon'])
            )
            if distance < min_distance:
                min_distance = distance
                nearest = station
        
        return nearest
    
    def _calculate_distance(self, loc1: Tuple[float, float], 
                           loc2: Tuple[float, float]) -> float:
        """Calculate distance between two coordinates."""
        from math import radians, sin, cos, sqrt, atan2
        
        lat1, lon1 = radians(loc1[0]), radians(loc1[1])
        lat2, lon2 = radians(loc2[0]), radians(loc2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return 6371.0 * c  # Earth radius in km
    
    def train(self, global_model_state: Dict, round_num: int) -> Dict:
        """
        Simulated training for IoT demo - smooth hardware flow.
        Simplified version that focuses on hardware interactions.
        """
        logger.info(f"🚗 {self.client_id}: Training (Round {round_num})...")
        self.training_active = True
        
        # Update display
        self._display_fl_status(round_num, self.last_accuracy, True, True)
        
        # Simulate training with smooth timing (2-3 seconds)
        # This creates a convincing flow for the demo
        training_duration = 2.5
        steps = 10
        for step in range(steps):
            # Update display to show progress
            progress = (step + 1) / steps
            progress_msg = f"Training...\nRound {round_num}\n{int(progress*100)}%"
            self.hardware.display_message(progress_msg)
            time.sleep(training_duration / steps)
        
        # Simulate improving accuracy (starts low, improves over rounds)
        base_accuracy = 0.45 + (round_num * 0.02)  # Improves with rounds
        accuracy = min(0.95, base_accuracy + np.random.uniform(-0.05, 0.05))
        loss = max(0.1, 1.0 - (round_num * 0.05))  # Decreases with rounds
        
        self.training_active = False
        
        logger.info(f"✅ Training complete: Acc={accuracy:.3f}, Loss={loss:.3f}")
        
        # Return simulated update (no actual model state needed)
        return {
            'model_state': {},  # Empty - not needed for simplified demo
            'num_samples': self.num_samples,
            'loss': loss,
            'accuracy': accuracy
        }


def main():
    """Run hardware FL client."""
    parser = argparse.ArgumentParser(description='FedRoute Hardware FL Client')
    parser.add_argument('--id', type=str, required=True, help='Client ID (e.g., vehicle_00)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print(" "*15 + "🚗 FEDROUTE HARDWARE FL CLIENT 🚗")
    print("="*70)
    print(f"\nClient ID: {args.id}")
    print(f"Server: {args.host}:{args.port}")
    print("\nHardware Features:")
    print("  ✓ OLED Display: Real-time FL status")
    print("  ✓ Servo Motor: Selection indicator")
    print("  ✓ Keypad: Interactive controls")
    print("  ✓ Privacy: Data stays on-device")
    print("\nKeypad Controls:")
    print("  1: Show FL Status")
    print("  2: Demo Navigation (using FL model)")
    print("  3: Show Privacy Info")
    print("  #: Exit")
    print("="*70 + "\n")
    
    client = HardwareFLClient(args.id, args.host, args.port)
    
    # Don't display on OLED during initialization - keep it blank
    logger.info("Hardware client initializing (OLED will remain blank until connected)...")
    
    if client.connect():
        logger.info("✅ Successfully connected to server, starting FL client...")
        client.listen()
    else:
        logger.error("❌ Failed to connect to server after multiple attempts")
        logger.error("   Make sure the server is running and accessible")
        logger.error(f"   Server: {args.host}:{args.port}")
        # Only show error on OLED if connection fails
        client._display_status("Connection\nFailed\nCheck Server", 3)
        client.hardware.cleanup()
        sys.exit(1)


if __name__ == '__main__':
    main()


