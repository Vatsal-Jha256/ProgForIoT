#!/usr/bin/env python3
"""
Option 1: Full Federated Learning Demo
Demonstrates the complete FedRoute federated learning workflow
STANDALONE VERSION - No dependencies on parent repo

Author: FedRoute Team
Date: 2025
"""

import time
import numpy as np
from hardware_controller import HardwareController


class FederatedLearningDemo:
    """
    Demonstrates federated learning workflow with hardware visualization.
    Standalone version - uses mock models for presentation.
    """
    
    def __init__(self, hardware: HardwareController):
        """Initialize FL demo."""
        self.hardware = hardware
        
        # Simulated clients
        self.num_clients = 5
        self.clients_selected_per_round = 3
        self.total_rounds = 5
        
        # Metrics
        self.round_accuracies = []
    
    def run(self):
        """Run the federated learning demo."""
        self.hardware.display_message("FedRoute FL Demo\n\nInitializing...")
        time.sleep(1)
        
        # Animate servo to show initialization
        self.hardware.servo_animation(0, 90, 10, 0.05)
        
        # Show welcome message
        self.hardware.display_message("Federated Learning\nDemo\n\nPress any key\nto start")
        self.hardware.get_key(timeout=10)
        
        # Run FL rounds
        for round_num in range(1, self.total_rounds + 1):
            self._run_fl_round(round_num)
            time.sleep(1)
        
        # Show final results
        self._show_final_results()
        
        # Return to menu
        self.hardware.display_message("Demo Complete!\n\nPress any key\nto return")
        self.hardware.get_key(timeout=10)
    
    def _run_fl_round(self, round_num: int):
        """Run a single FL round."""
        # Round start
        self.hardware.display_message(f"Round {round_num}/{self.total_rounds}\n\nConnecting clients...")
        self.hardware.servo_animation(90, 45, 5, 0.03)
        time.sleep(0.5)
        
        # Client selection
        selected_clients = np.random.choice(
            self.num_clients, 
            size=self.clients_selected_per_round, 
            replace=False
        )
        
        self.hardware.display_message(
            f"Round {round_num}\n"
            f"Selected: {len(selected_clients)} clients\n"
            f"IDs: {', '.join([f'V{i+1}' for i in selected_clients])}"
        )
        self.hardware.servo_animation(45, 135, 8, 0.03)
        time.sleep(1)
        
        # Model broadcast
        self.hardware.display_message(
            f"Round {round_num}\n"
            f"Broadcasting global\nmodel to clients..."
        )
        time.sleep(0.8)
        
        # Local training simulation
        self.hardware.display_message(
            f"Round {round_num}\n"
            f"Local training\nin progress..."
        )
        
        # Animate servo during training
        for _ in range(3):
            self.hardware.servo_animation(90, 135, 5, 0.05)
            self.hardware.servo_animation(135, 45, 5, 0.05)
            time.sleep(0.3)
        
        # Simulate training progress
        training_steps = 5
        for step in range(training_steps):
            progress = int((step + 1) / training_steps * 100)
            self.hardware.display_message(
                f"Round {round_num}\n"
                f"Training: {progress}%\n"
                f"Privacy: Active"
            )
            time.sleep(0.3)
        
        # Aggregation
        self.hardware.display_message(
            f"Round {round_num}\n"
            f"Aggregating updates\nwith DP noise..."
        )
        self.hardware.servo_animation(45, 90, 5, 0.05)
        time.sleep(0.8)
        
        # Calculate simulated accuracy (improving over rounds)
        base_accuracy = 0.65 + (round_num - 1) * 0.03 + np.random.uniform(-0.02, 0.02)
        base_accuracy = min(0.95, max(0.60, base_accuracy))
        
        path_acc = base_accuracy + np.random.uniform(-0.02, 0.02)
        music_acc = base_accuracy + np.random.uniform(-0.02, 0.02)
        combined_acc = (path_acc + music_acc) / 2
        
        self.round_accuracies.append({
            'round': round_num,
            'path': path_acc,
            'music': music_acc,
            'combined': combined_acc
        })
        
        # Show results
        self.hardware.display_message(
            f"Round {round_num} Complete\n\n"
            f"Path Acc: {path_acc:.3f}\n"
            f"Music Acc: {music_acc:.3f}\n"
            f"Combined: {combined_acc:.3f}"
        )
        
        # Success animation
        self.hardware.servo_animation(90, 180, 10, 0.03)
        self.hardware.servo_animation(180, 0, 10, 0.03)
        self.hardware.servo_animation(0, 90, 10, 0.03)
        
        time.sleep(2)
    
    def _show_final_results(self):
        """Show final FL results."""
        if not self.round_accuracies:
            return
        
        final = self.round_accuracies[-1]
        
        self.hardware.display_message(
            "Training Complete!\n\n"
            f"Final Accuracy:\n"
            f"Path: {final['path']:.3f}\n"
            f"Music: {final['music']:.3f}\n"
            f"Combined: {final['combined']:.3f}"
        )
        
        # Celebration animation
        for _ in range(3):
            self.hardware.servo_animation(0, 180, 15, 0.02)
            self.hardware.servo_animation(180, 0, 15, 0.02)
        
        time.sleep(2)
        
        # Show privacy summary
        self.hardware.display_message(
            "Privacy Summary:\n\n"
            "✓ Data stays local\n"
            "✓ DP noise added\n"
            "✓ Secure aggregation\n"
            "✓ No raw data shared"
        )
        time.sleep(3)


if __name__ == "__main__":
    # Test the demo
    hardware = HardwareController(simulation_mode=True)
    demo = FederatedLearningDemo(hardware)
    demo.run()
    hardware.cleanup()
