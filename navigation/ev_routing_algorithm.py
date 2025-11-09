#!/usr/bin/env python3
"""
EV Routing Algorithm
A* pathfinding for optimal route calculation to charging stations
"""

import math
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger("EVRouting")


class EVRoutingAlgorithm:
    """A* pathfinding algorithm for EV navigation"""
    
    def __init__(self):
        """Initialize routing algorithm"""
        # Road network would be loaded from OSM data in real implementation
        # For now, we use simplified waypoint-based routing
        self.waypoints = self._create_bhubaneswar_waypoints()
        logger.info("✅ Routing algorithm initialized")
    
    def _create_bhubaneswar_waypoints(self) -> List[Dict]:
        """Create waypoints for Bhubaneswar road network"""
        # Key intersections and landmarks in Bhubaneswar
        return [
            {'id': 'W01', 'lat': 20.2961, 'lon': 85.8245, 'name': 'City Center'},
            {'id': 'W02', 'lat': 20.2644, 'lon': 85.8281, 'name': 'KIIT Junction'},
            {'id': 'W03', 'lat': 20.3100, 'lon': 85.8500, 'name': 'Patia Square'},
            {'id': 'W04', 'lat': 20.2800, 'lon': 85.8000, 'name': 'Old Town'},
            {'id': 'W05', 'lat': 20.3200, 'lon': 85.8200, 'name': 'Nayapalli'},
            {'id': 'W06', 'lat': 20.2500, 'lon': 85.8500, 'name': 'Railway Station'},
            {'id': 'W07', 'lat': 20.3000, 'lon': 85.8800, 'name': 'Airport Road'},
            {'id': 'W08', 'lat': 20.2700, 'lon': 85.7800, 'name': 'Lingaraj Area'},
        ]
    
    def calculate_route(self, start: Tuple[float, float], 
                       end: Tuple[float, float]) -> Optional[List[Dict]]:
        """
        Calculate route from start to end using A* algorithm
        
        Args:
            start: (lat, lon) starting point
            end: (lat, lon) destination point
            
        Returns:
            List of route steps with direction, distance, heading, ETA
        """
        try:
            # Find nearest waypoints
            start_wp = self._find_nearest_waypoint(start)
            end_wp = self._find_nearest_waypoint(end)
            
            if not start_wp or not end_wp:
                logger.warning("Could not find waypoints")
                return self._create_direct_route(start, end)
            
            # Use A* to find path through waypoints
            path = self._astar_search(start_wp, end_wp)
            
            if not path:
                logger.warning("A* search failed, using direct route")
                return self._create_direct_route(start, end)
            
            # Convert path to navigation steps
            route_steps = self._path_to_steps(path, start, end)
            
            logger.info(f"✅ Route calculated: {len(route_steps)} steps")
            return route_steps
            
        except Exception as e:
            logger.error(f"❌ Route calculation error: {e}")
            return self._create_direct_route(start, end)
    
    def _astar_search(self, start: Dict, goal: Dict) -> Optional[List[Dict]]:
        """A* pathfinding algorithm"""
        # Simplified A* - in real implementation, would use full road network
        open_set = [start]
        came_from = {}
        g_score = {start['id']: 0}
        f_score = {start['id']: self._heuristic(start, goal)}
        
        while open_set:
            # Get node with lowest f_score
            current = min(open_set, key=lambda n: f_score.get(n['id'], float('inf')))
            
            if current['id'] == goal['id']:
                # Reconstruct path
                path = [current]
                while current['id'] in came_from:
                    current = came_from[current['id']]
                    path.append(current)
                path.reverse()
                return path
            
            open_set.remove(current)
            
            # Get neighbors (simplified - all waypoints are connected)
            for neighbor in self.waypoints:
                if neighbor['id'] == current['id']:
                    continue
                
                tentative_g = g_score[current['id']] + self._calculate_distance(
                    (current['lat'], current['lon']),
                    (neighbor['lat'], neighbor['lon'])
                )
                
                neighbor_id = neighbor['id']
                if neighbor_id not in g_score or tentative_g < g_score[neighbor_id]:
                    came_from[neighbor_id] = current
                    g_score[neighbor_id] = tentative_g
                    f_score[neighbor_id] = tentative_g + self._heuristic(neighbor, goal)
                    
                    if neighbor not in open_set:
                        open_set.append(neighbor)
        
        return None  # No path found
    
    def _heuristic(self, node: Dict, goal: Dict) -> float:
        """Heuristic function (Euclidean distance)"""
        return self._calculate_distance(
            (node['lat'], node['lon']),
            (goal['lat'], goal['lon'])
        )
    
    def _find_nearest_waypoint(self, location: Tuple[float, float]) -> Optional[Dict]:
        """Find nearest waypoint to given location"""
        if not self.waypoints:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for wp in self.waypoints:
            distance = self._calculate_distance(
                location,
                (wp['lat'], wp['lon'])
            )
            if distance < min_distance:
                min_distance = distance
                nearest = wp
        
        return nearest
    
    def _path_to_steps(self, path: List[Dict], 
                      start: Tuple[float, float],
                      end: Tuple[float, float]) -> List[Dict]:
        """Convert path to navigation steps"""
        steps = []
        
        # Add initial step from start to first waypoint
        if path:
            first_wp = path[0]
            distance = self._calculate_distance(start, (first_wp['lat'], first_wp['lon']))
            heading = self._calculate_heading(start, (first_wp['lat'], first_wp['lon']))
            direction = self._heading_to_direction(heading)
            
            steps.append({
                'waypoint': first_wp['name'],
                'distance': distance,
                'heading': heading,
                'direction': direction,
                'eta': distance * 2.5  # Assume 40 km/h average speed
            })
        
        # Add steps between waypoints
        for i in range(len(path) - 1):
            current = path[i]
            next_wp = path[i + 1]
            
            distance = self._calculate_distance(
                (current['lat'], current['lon']),
                (next_wp['lat'], next_wp['lon'])
            )
            heading = self._calculate_heading(
                (current['lat'], current['lon']),
                (next_wp['lat'], next_wp['lon'])
            )
            direction = self._heading_to_direction(heading)
            
            steps.append({
                'waypoint': next_wp['name'],
                'distance': distance,
                'heading': heading,
                'direction': direction,
                'eta': distance * 2.5
            })
        
        # Add final step to destination
        if path:
            last_wp = path[-1]
            distance = self._calculate_distance((last_wp['lat'], last_wp['lon']), end)
            heading = self._calculate_heading((last_wp['lat'], last_wp['lon']), end)
            direction = self._heading_to_direction(heading)
            
            steps.append({
                'waypoint': 'Destination',
                'distance': distance,
                'heading': heading,
                'direction': direction,
                'eta': distance * 2.5
            })
        
        return steps
    
    def _create_direct_route(self, start: Tuple[float, float], 
                            end: Tuple[float, float]) -> List[Dict]:
        """Create simple direct route when pathfinding fails"""
        distance = self._calculate_distance(start, end)
        heading = self._calculate_heading(start, end)
        direction = self._heading_to_direction(heading)
        
        return [{
            'waypoint': 'Destination',
            'distance': distance,
            'heading': heading,
            'direction': direction,
            'eta': distance * 2.5
        }]
    
    def _calculate_distance(self, loc1: Tuple[float, float], 
                           loc2: Tuple[float, float]) -> float:
        """Calculate distance using Haversine formula"""
        lat1, lon1 = math.radians(loc1[0]), math.radians(loc1[1])
        lat2, lon2 = math.radians(loc2[0]), math.radians(loc2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return 6371.0 * c  # Earth radius in km
    
    def _calculate_heading(self, start: Tuple[float, float], 
                          end: Tuple[float, float]) -> float:
        """Calculate heading/bearing from start to end in degrees"""
        lat1, lon1 = math.radians(start[0]), math.radians(start[1])
        lat2, lon2 = math.radians(end[0]), math.radians(end[1])
        
        dlon = lon2 - lon1
        
        y = math.sin(dlon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        
        heading = math.atan2(y, x)
        heading = math.degrees(heading)
        heading = (heading + 360) % 360  # Normalize to 0-360
        
        return heading
    
    def _heading_to_direction(self, heading: float) -> str:
        """Convert heading to direction string"""
        # Normalize heading
        heading = heading % 360
        
        # Determine direction based on heading
        if 315 <= heading or heading < 45:
            return "STRAIGHT"  # North
        elif 45 <= heading < 135:
            return "RIGHT"  # East
        elif 135 <= heading < 225:
            return "STRAIGHT"  # South (continue)
        else:  # 225 <= heading < 315
            return "LEFT"  # West


