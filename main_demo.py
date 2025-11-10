#!/usr/bin/env python3
"""
FedRoute Hardware Demo - Main Interactive Menu
Complete hardware demonstration with keypad navigation
STANDALONE VERSION - No dependencies on parent repo

Author: FedRoute Team
Date: 2025
"""

import sys
import time
from pathlib import Path

# Add hardware_demo to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from hardware_controller import HardwareController
from demo_federated_learning import FederatedLearningDemo
from demo_poi_navigation import POINavigationDemo
from demo_system_info import SystemInfoDemo


class FedRouteHardwareDemo:
    """
    Main interactive demo with menu system.
    """
    
    def __init__(self, simulation_mode: bool = False):
        """Initialize main demo."""
        self.hardware = HardwareController(simulation_mode=simulation_mode)
        self.running = True
        
        # Menu options
        self.menu_options = [
            "Federated Learning Demo",
            "POI & Navigation Demo",
            "System Information"
        ]
        
        print("\n" + "="*60)
        print("🚀 FedRoute Hardware Demo")
        print("="*60)
        print("\nInitializing hardware...")
    
    def run(self):
        """Run the main demo loop."""
        try:
            # Show welcome screen
            self._show_welcome()
            
            # Main menu loop
            while self.running:
                self._show_main_menu()
                selection = self._get_menu_selection()
                
                if selection == '4':
                    self._run_fl_demo()
                elif selection == '5':
                    self._run_poi_demo()
                elif selection == '6':
                    self._run_system_info_demo()
                elif selection == '*':
                    # Exit option
                    self._show_exit_message()
                    break
                elif selection is None:
                    # Timeout or invalid key
                    continue
                else:
                    # Invalid selection
                    self.hardware.display_message(
                        "Invalid Selection\n\n"
                        "Please choose 4-6\n"
                        "or * to exit"
                    )
                    time.sleep(2)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted by user")
            self._show_exit_message()
        
        finally:
            self.cleanup()
    
    def _show_welcome(self):
        """Show welcome screen."""
        self.hardware.display_message(
            "FedRoute\n"
            "Hardware Demo\n\n"
            "Privacy-Preserving\n"
            "Federated Learning\n"
            "for IoV"
        )
        
        # Welcome animation
        self.hardware.servo_animation(0, 180, 20, 0.03)
        self.hardware.servo_animation(180, 0, 20, 0.03)
        self.hardware.set_servo_angle(90)
        
        time.sleep(2)
        
        self.hardware.display_message(
            "Welcome!\n\n"
            "Press any key\nto continue"
        )
        self.hardware.get_key(timeout=10)
    
    def _show_main_menu(self):
        """Display main menu."""
        menu_text = "Main Menu\n\n"
        # Use keys 4, 5, 6 (since 1, 2, 3 don't work)
        for i, option in enumerate(self.menu_options, 4):
            menu_text += f"{i}. {option}\n"
        menu_text += "\n* = Exit"
        
        self.hardware.display_message(menu_text)
        
        # Menu indicator animation
        self.hardware.servo_animation(90, 135, 5, 0.05)
        self.hardware.servo_animation(135, 45, 5, 0.05)
        self.hardware.set_servo_angle(90)
    
    def _get_menu_selection(self) -> str:
        """
        Get menu selection from keypad.
        Uses keys 4, 5, 6 (1, 2, 3, A don't work).
        
        Returns:
            Selected key or None
        """
        key = self.hardware.get_key(timeout=30)
        
        if key in ['4', '5', '6', '*']:
            return key
        
        return None
    
    def _run_fl_demo(self):
        """Run federated learning demo."""
        try:
            demo = FederatedLearningDemo(self.hardware)
            demo.run()
        except Exception as e:
            print(f"Error in FL demo: {e}")
            self.hardware.display_message(
                "Demo Error\n\n"
                "Returning to menu..."
            )
            time.sleep(2)
    
    def _run_poi_demo(self):
        """Run POI navigation demo."""
        try:
            demo = POINavigationDemo(self.hardware)
            demo.run()
        except Exception as e:
            print(f"Error in POI demo: {e}")
            self.hardware.display_message(
                "Demo Error\n\n"
                "Returning to menu..."
            )
            time.sleep(2)
    
    def _run_system_info_demo(self):
        """Run system information demo."""
        try:
            demo = SystemInfoDemo(self.hardware)
            demo.run()
        except Exception as e:
            print(f"Error in system info demo: {e}")
            self.hardware.display_message(
                "Demo Error\n\n"
                "Returning to menu..."
            )
            time.sleep(2)
    
    def _show_exit_message(self):
        """Show exit message."""
        self.hardware.display_message(
            "Thank You!\n\n"
            "FedRoute Demo\n"
            "Complete\n\n"
            "Goodbye!"
        )
        
        # Exit animation
        for _ in range(2):
            self.hardware.servo_animation(0, 180, 15, 0.02)
            self.hardware.servo_animation(180, 0, 15, 0.02)
        
        self.hardware.set_servo_angle(90)
        time.sleep(2)
    
    def cleanup(self):
        """Clean up resources."""
        print("\nCleaning up...")
        self.hardware.cleanup()
        print("✅ Demo complete!\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='FedRoute Hardware Demo')
    parser.add_argument(
        '--simulation',
        action='store_true',
        help='Run in simulation mode (no hardware required)'
    )
    
    args = parser.parse_args()
    
    demo = FedRouteHardwareDemo(simulation_mode=args.simulation)
    demo.run()


if __name__ == "__main__":
    main()
