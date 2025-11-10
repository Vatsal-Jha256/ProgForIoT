#!/usr/bin/env python3
"""
Option 2: POI Finding and Navigation with Music Recommendations
Demonstrates intelligent POI recommendations and music suggestions
STANDALONE VERSION - Uses NYC-specific data

Author: FedRoute Team
Date: 2025
"""

import time
import numpy as np
from hardware_controller import HardwareController


class POINavigationDemo:
    """
    Demonstrates POI finding and navigation with music recommendations.
    Uses NYC-specific POIs and music data.
    """
    
    def __init__(self, hardware: HardwareController):
        """Initialize POI navigation demo."""
        self.hardware = hardware
        
        # NYC POI categories (from NYC dataset)
        self.poi_categories = [
            "Restaurant", "Cinema", "Museum", "Theater", 
            "Park", "Shopping", "Train Station", "Library",
            "Airport", "Beach"
        ]
        
        # NYC POIs with realistic locations, data, and bearing angles
        # Bearing: 0°=North, 90°=East, 180°=South, 270°=West (mapped to 0-180° servo range)
        self.nyc_pois = [
            {"name": "Central Park", "category": "Park", "distance": 2.3, "rating": 4.8, "area": "Manhattan", "bearing": 45},  # Northeast
            {"name": "Times Square", "category": "Shopping", "distance": 1.2, "rating": 4.5, "area": "Manhattan", "bearing": 0},  # North
            {"name": "Empire State Bldg", "category": "Museum", "distance": 0.8, "rating": 4.7, "area": "Manhattan", "bearing": 90},  # East
            {"name": "Broadway Theater", "category": "Theater", "distance": 1.5, "rating": 4.9, "area": "Manhattan", "bearing": 135},  # Southeast
            {"name": "AMC Cinema", "category": "Cinema", "distance": 3.1, "rating": 4.4, "area": "Manhattan", "bearing": 180},  # South
            {"name": "NY Public Library", "category": "Library", "distance": 1.8, "rating": 4.6, "area": "Manhattan", "bearing": 22},  # North-Northeast
            {"name": "JFK Airport", "category": "Airport", "distance": 15.2, "rating": 4.3, "area": "Queens", "bearing": 90},  # East
            {"name": "Coney Island", "category": "Beach", "distance": 12.5, "rating": 4.2, "area": "Brooklyn", "bearing": 180},  # South
            {"name": "Grand Central", "category": "Train Station", "distance": 0.5, "rating": 4.7, "area": "Manhattan", "bearing": 45},  # Northeast
            {"name": "Joe's Pizza", "category": "Restaurant", "distance": 2.1, "rating": 4.6, "area": "Manhattan", "bearing": 67},  # East-Northeast
            {"name": "MoMA", "category": "Museum", "distance": 2.8, "rating": 4.8, "area": "Manhattan", "bearing": 112},  # East-Southeast
            {"name": "Brooklyn Bridge", "category": "Park", "distance": 3.5, "rating": 4.9, "area": "Brooklyn", "bearing": 157},  # South-Southeast
        ]
        
        # NYC music genres and tracks (based on NYC music data)
        self.music_genres = [
            "Jazz", "Hip Hop", "Rock", "Electronic", "R&B",
            "Blues", "Classical", "Indie", "Punk", "Reggae"
        ]
        
        # Music recommendations by POI category (NYC-style)
        self.music_by_category = {
            "Park": {
                "genre": "Indie",
                "tracks": ["Central Park", "Brooklyn Nights", "NYC Dreams"]
            },
            "Shopping": {
                "genre": "Hip Hop",
                "tracks": ["Empire State", "Big Apple", "City Lights"]
            },
            "Museum": {
                "genre": "Classical",
                "tracks": ["Museum Walk", "Art Gallery", "Cultural Vibes"]
            },
            "Theater": {
                "genre": "Jazz",
                "tracks": ["Broadway Blues", "Showtime", "Stage Lights"]
            },
            "Cinema": {
                "genre": "Electronic",
                "tracks": ["Movie Magic", "Screen Time", "Cinema Vibes"]
            },
            "Restaurant": {
                "genre": "Jazz",
                "tracks": ["Dinner Music", "NYC Bistro", "City Eats"]
            },
            "Train Station": {
                "genre": "Rock",
                "tracks": ["Subway Song", "Train Tracks", "Metro Beat"]
            },
            "Library": {
                "genre": "Classical",
                "tracks": ["Quiet Study", "Reading Room", "Knowledge"]
            },
            "Airport": {
                "genre": "Electronic",
                "tracks": ["Takeoff", "Flight Mode", "Departure"]
            },
            "Beach": {
                "genre": "Reggae",
                "tracks": ["Beach Vibes", "Ocean Waves", "Summer NY"]
            }
        }
        
        # Current location (NYC - Manhattan center)
        self.current_location = (40.7589, -73.9851)  # Times Square area
    
    def run(self):
        """Run the POI navigation demo."""
        self.hardware.display_message("POI Navigation\nDemo\n\nInitializing...")
        time.sleep(1)
        
        # Animate servo
        self.hardware.servo_animation(0, 90, 10, 0.05)
        
        # Show welcome
        self.hardware.display_message("NYC POI & Navigation\nDemo\n\nPress any key\nto start")
        self.hardware.get_key(timeout=10)
        
        # Step 1: Get current context
        self._show_current_context()
        
        # Step 2: Find relevant POIs
        recommended_pois = self._find_relevant_pois()
        
        # Step 3: Display POI recommendations
        self._display_poi_recommendations(recommended_pois)
        
        # Step 4: Select a POI and navigate
        selected_poi = self._select_poi(recommended_pois)
        if selected_poi:
            self._navigate_to_poi(selected_poi)
        
        # Step 5: Get music recommendations
        self._show_music_recommendations(selected_poi if selected_poi else recommended_pois[0])
        
        # Step 6: Show complete journey
        self._show_journey_summary(selected_poi if selected_poi else recommended_pois[0])
        
        # Return to menu
        self.hardware.display_message("Demo Complete!\n\nPress any key\nto return")
        self.hardware.get_key(timeout=10)
    
    def _show_current_context(self):
        """Show current vehicle context."""
        self.hardware.display_message(
            "Analyzing Context...\n\n"
            "Location: NYC Manhattan\n"
            "Time: Afternoon\n"
            "Traffic: Moderate"
        )
        # Servo sweeps to show analysis in progress
        self.hardware.servo_animation(45, 135, 8, 0.03)
        time.sleep(2)
        
        self.hardware.display_message(
            "Context Analysis\nComplete\n\n"
            "Using FL model\nfor predictions..."
        )
        # Return servo to center (ready position)
        self.hardware.set_servo_angle(90)
        time.sleep(1.5)
    
    def _find_relevant_pois(self):
        """Find relevant POIs using FL model (simulated)."""
        self.hardware.display_message(
            "Finding Relevant\nPOIs...\n\n"
            "Using FL model..."
        )
        
        # Simulate model inference - select POIs based on context
        # In real system, this would use the FL model
        # For demo: prioritize nearby, high-rated POIs
        
        # Filter by distance and rating
        nearby_pois = [poi for poi in self.nyc_pois if poi['distance'] < 5.0]
        nearby_pois.sort(key=lambda x: (x['distance'], -x['rating']))
        
        # Select top 3
        recommended_pois = nearby_pois[:3]
        
        # If not enough nearby, add some popular ones
        if len(recommended_pois) < 3:
            popular = sorted(self.nyc_pois, key=lambda x: -x['rating'])[:3]
            for poi in popular:
                if poi not in recommended_pois:
                    recommended_pois.append(poi)
                    if len(recommended_pois) >= 3:
                        break
        
        recommended_pois = recommended_pois[:3]
        
        # Servo sweeps to show POI search in progress
        self.hardware.servo_animation(135, 45, 10, 0.03)
        # Return to center after search
        self.hardware.set_servo_angle(90)
        time.sleep(1)
        
        return recommended_pois
    
    def _display_poi_recommendations(self, pois):
        """Display POI recommendations."""
        self.hardware.display_message(
            "Top Recommendations:\n\n"
            f"4. {pois[0]['name']}\n"
            f"   {pois[0]['distance']}km, {pois[0]['rating']}★"
        )
        time.sleep(2)
        
        if len(pois) > 1:
            self.hardware.display_message(
                "Top Recommendations:\n\n"
                f"5. {pois[1]['name']}\n"
                f"   {pois[1]['distance']}km, {pois[1]['rating']}★"
            )
            time.sleep(2)
        
        if len(pois) > 2:
            self.hardware.display_message(
                "Top Recommendations:\n\n"
                f"6. {pois[2]['name']}\n"
                f"   {pois[2]['distance']}km, {pois[2]['rating']}★"
            )
            time.sleep(2)
    
    def _select_poi(self, pois):
        """Let user select a POI."""
        self.hardware.display_message(
            "Select POI:\n\n"
            "Press 4-6 to select\n"
            "or * to skip"
        )
        
        key = self.hardware.get_key(timeout=10)
        
        if key and key in ['4', '5', '6']:
            idx = int(key) - 4  # Map 4->0, 5->1, 6->2
            if idx < len(pois):
                selected = pois[idx]
                self.hardware.display_message(
                    f"Selected:\n{selected['name']}\n\n"
                    f"Distance: {selected['distance']}km"
                )
                # Point servo in direction of selected POI
                bearing = selected.get('bearing', 90)
                self.hardware.servo_animation(90, bearing, 10, 0.03)
                time.sleep(1.5)
                return selected
        
        # Default to first POI
        selected = pois[0]
        # Point servo in direction of default POI
        bearing = selected.get('bearing', 90)
        self.hardware.servo_animation(90, bearing, 10, 0.03)
        return selected
    
    def _navigate_to_poi(self, poi):
        """
        Simulate navigation to POI with directional servo pointing.
        Servo acts as a compass, pointing in the direction of the destination.
        """
        bearing = poi.get('bearing', 90)  # Direction to POI (0-180°)
        
        self.hardware.display_message(
            "Starting Navigation\n\n"
            f"Destination:\n{poi['name']}\n"
            f"Distance: {poi['distance']}km"
        )
        # Point servo in initial direction
        self.hardware.servo_animation(90, bearing, 10, 0.05)
        time.sleep(1.5)
        
        # Simulate navigation progress with directional updates
        steps = 8
        current_bearing = bearing
        
        for i in range(steps):
            progress = int((i + 1) / steps * 100)
            distance_remaining = poi['distance'] * (1 - (i + 1) / steps)
            
            # Simulate slight direction changes during navigation (realistic route adjustments)
            # Add small variations to simulate turns and route corrections
            bearing_variation = np.random.uniform(-10, 10)
            target_bearing = max(0, min(180, bearing + bearing_variation))
            
            self.hardware.display_message(
                f"Navigating...\n\n"
                f"Progress: {progress}%\n"
                f"Remaining: {distance_remaining:.1f}km\n"
                f"→ {self._bearing_to_direction(target_bearing)}"
            )
            
            # Smoothly update servo to point in current direction
            self.hardware.servo_animation(current_bearing, target_bearing, 5, 0.05)
            current_bearing = target_bearing
            time.sleep(0.6)
        
        # Final approach - point directly at destination
        self.hardware.servo_animation(current_bearing, bearing, 8, 0.03)
        time.sleep(0.5)
        
        self.hardware.display_message(
            "Arrived!\n\n"
            f"Welcome to\n{poi['name']}"
        )
        
        # Success animation - quick sweep to celebrate arrival
        self.hardware.servo_animation(bearing, bearing + 30, 5, 0.02)
        self.hardware.servo_animation(bearing + 30, bearing - 30, 5, 0.02)
        self.hardware.servo_animation(bearing - 30, bearing, 5, 0.02)
        time.sleep(2)
    
    def _bearing_to_direction(self, bearing):
        """Convert bearing angle to cardinal direction string."""
        if bearing < 22.5:
            return "N"
        elif bearing < 67.5:
            return "NE"
        elif bearing < 112.5:
            return "E"
        elif bearing < 157.5:
            return "SE"
        else:
            return "S"
    
    def _show_music_recommendations(self, poi):
        """Show music recommendations based on context."""
        self.hardware.display_message(
            "Music Recommendations\n\n"
            "Analyzing context..."
        )
        time.sleep(1)
        
        # Get music for POI category
        music_info = self.music_by_category.get(
            poi['category'],
            {"genre": "Jazz", "tracks": ["NYC Vibes", "City Sounds", "Urban Beat"]}
        )
        
        self.hardware.display_message(
            "Recommended Music:\n\n"
            f"Genre: {music_info['genre']}\n"
            f"Track 1: {music_info['tracks'][0]}\n"
            f"Track 2: {music_info['tracks'][1]}"
        )
        
        # Animate servo to music rhythm (gentle back-and-forth)
        for _ in range(3):
            self.hardware.servo_animation(60, 120, 6, 0.08)
            self.hardware.servo_animation(120, 60, 6, 0.08)
        
        # Return to center after music animation
        self.hardware.set_servo_angle(90)
        time.sleep(3)
        
        self.hardware.display_message(
            "Music Playing:\n\n"
            f"Now: {music_info['tracks'][0]}\n"
            f"Next: {music_info['tracks'][1]}\n"
            f"Genre: {music_info['genre']}"
        )
        time.sleep(2)
    
    def _show_journey_summary(self, poi):
        """Show complete journey summary."""
        self.hardware.display_message(
            "Journey Summary\n\n"
            f"Destination: {poi['name']}\n"
            f"Distance: {poi['distance']}km\n"
            f"Status: Complete"
        )
        time.sleep(2)
        
        self.hardware.display_message(
            "FedRoute Features:\n\n"
            "✓ POI Recommendation\n"
            "✓ Music Suggestion\n"
            "✓ Privacy Preserved\n"
            "✓ FL Model Used"
        )
        
        # Final celebration animation - full sweep
        for _ in range(2):
            self.hardware.servo_animation(0, 180, 20, 0.02)
            self.hardware.servo_animation(180, 0, 20, 0.02)
        # Return to center/ready position
        self.hardware.set_servo_angle(90)
        
        time.sleep(3)


if __name__ == "__main__":
    # Test the demo
    hardware = HardwareController(simulation_mode=True)
    demo = POINavigationDemo(hardware)
    demo.run()
    hardware.cleanup()
