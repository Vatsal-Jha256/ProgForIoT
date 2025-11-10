#!/usr/bin/env python3
"""
Option 3: System Information and Status Display
Shows system status, model info, and privacy features
STANDALONE VERSION - No dependencies on parent repo

Author: FedRoute Team
Date: 2025
"""

import time
from hardware_controller import HardwareController


class SystemInfoDemo:
    """
    Displays system information and status.
    Standalone version - uses mock data for presentation.
    """
    
    def __init__(self, hardware: HardwareController):
        """Initialize system info demo."""
        self.hardware = hardware
        
        # Mock model parameters (for presentation)
        self.total_params = 125000  # ~125K parameters
        self.trainable_params = 125000
    
    def run(self):
        """Run the system info demo."""
        self.hardware.display_message("System Information\n\nLoading...")
        time.sleep(1)
        
        # Show model information
        self._show_model_info()
        time.sleep(2)
        
        # Show privacy features
        self._show_privacy_features()
        time.sleep(2)
        
        # Show system architecture
        self._show_architecture()
        time.sleep(2)
        
        # Show key features
        self._show_key_features()
        time.sleep(2)
        
        # Return to menu
        self.hardware.display_message("Info Complete!\n\nPress any key\nto return")
        self.hardware.get_key(timeout=10)
    
    def _show_model_info(self):
        """Show model information."""
        self.hardware.display_message(
            "Model Information\n\n"
            f"Total Params: {self.total_params//1000}K\n"
            f"Trainable: {self.trainable_params//1000}K\n"
            f"Architecture: FMTL"
        )
        
        # Animate servo
        self.hardware.servo_animation(45, 135, 10, 0.03)
        time.sleep(2)
        
        self.hardware.display_message(
            "Model Details:\n\n"
            "Shared Encoder:\n"
            "64→128→256→128\n"
            "Task Heads: 2"
        )
        time.sleep(2)
    
    def _show_privacy_features(self):
        """Show privacy features."""
        self.hardware.display_message(
            "Privacy Features\n\n"
            "✓ Differential Privacy\n"
            "✓ Secure Aggregation\n"
            "✓ Local Training"
        )
        
        # Privacy animation
        for _ in range(2):
            self.hardware.servo_animation(90, 180, 10, 0.03)
            self.hardware.servo_animation(180, 0, 10, 0.03)
        
        time.sleep(2)
        
        self.hardware.display_message(
            "Privacy Guarantees:\n\n"
            "ε-DP: 1.0\n"
            "δ-DP: 1e-5\n"
            "Data: On-device"
        )
        time.sleep(2)
    
    def _show_architecture(self):
        """Show system architecture."""
        self.hardware.display_message(
            "System Architecture\n\n"
            "FedRoute Framework\n"
            "Client-Server FL\n"
            "Multi-Task Learning"
        )
        time.sleep(2)
        
        self.hardware.display_message(
            "Components:\n\n"
            "• FL Server\n"
            "• Vehicle Clients\n"
            "• FMTL Model\n"
            "• Privacy Engine"
        )
        
        # Architecture animation
        self.hardware.servo_animation(0, 180, 15, 0.02)
        self.hardware.set_servo_angle(90)
        time.sleep(2)
    
    def _show_key_features(self):
        """Show key features."""
        features = [
            "Key Features:\n\n✓ POI Recommendations\n✓ Music Suggestions\n✓ Privacy Preserved",
            "Key Features:\n\n✓ Context-Aware\n✓ Multi-Task Learning\n✓ Federated Training",
            "Key Features:\n\n✓ On-Device Data\n✓ Secure Updates\n✓ Real-time Inference"
        ]
        
        for feature_text in features:
            self.hardware.display_message(feature_text)
            self.hardware.servo_animation(45, 135, 5, 0.05)
            time.sleep(2)
        
        # Final summary
        self.hardware.display_message(
            "FedRoute System\n\n"
            "Privacy-Preserving\n"
            "Federated Learning\n"
            "for IoV"
        )
        
        # Final animation
        self.hardware.servo_animation(0, 180, 20, 0.02)
        self.hardware.servo_animation(180, 0, 20, 0.02)
        self.hardware.set_servo_angle(90)
        
        time.sleep(2)


if __name__ == "__main__":
    # Test the demo
    hardware = HardwareController(simulation_mode=True)
    demo = SystemInfoDemo(hardware)
    demo.run()
    hardware.cleanup()
