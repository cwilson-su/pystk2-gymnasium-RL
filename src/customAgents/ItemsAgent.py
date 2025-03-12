import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.TrackUtils import compute_curvature, compute_slope

class ItemsAgent:
    """Agent that follows the track while avoiding ALL items (with peripheral vision)."""
    def __init__(self, track, render_mode=None, num_kart=2, path_lookahead=3, forecast_distance=5, peripheral_angle=30):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.path_lookahead = path_lookahead
        self.forecast_distance = forecast_distance  # Distance to look ahead for items
        self.peripheral_angle = np.radians(peripheral_angle)  # Peripheral vision angle in radians
        self.obs = None
        self.agent_positions = []

    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def is_in_peripheral_zone(self, item_pos, kart_front):
        """Check if an item is within the peripheral vision zone."""
        # Compute the direction vector to the item
        direction_to_item = item_pos / np.linalg.norm(item_pos)
        kart_direction = kart_front / np.linalg.norm(kart_front)
        
        # Compute angle between agent's direction and item
        angle = np.arccos(np.clip(np.dot(direction_to_item, kart_direction), -1.0, 1.0))
        return angle < self.peripheral_angle

    def calculate_action(self):
        """Compute the action to stay on track and handle item-based decisions."""
        if self.obs is None:
            return {}

        path_end = self.obs["paths_end"][self.path_lookahead - 1]
        kart_front = self.obs["front"]

        path_ends = self.obs["paths_end"][:self.path_lookahead]
        curvature = compute_curvature(path_ends)
        slope = compute_slope(path_ends[:2])

        # Base steering logic (like MedianAgent)
        direction_to_target = path_end - kart_front
        steering = 0.2 * direction_to_target[0]

        # Item avoidance logic (Avoid ALL items with peripheral vision)
        items_position = self.obs.get("items_position", [])
        paths_width = self.obs.get("paths_width", [1])[0]

        # Item detection logic
        best_move = 0  # Default: no movement adjustment
        for item_pos in items_position:
            # Check if item is within forecast distance
            distance_to_item = np.linalg.norm(item_pos)
            if distance_to_item < self.forecast_distance and self.is_in_peripheral_zone(item_pos, kart_front):
                # Always avoid items (for testing)
                if item_pos[0] > 0 and item_pos[0] < paths_width / 2:
                    best_move = -0.3  # Move left more aggressively
                elif item_pos[0] < 0 and abs(item_pos[0]) < paths_width / 2:
                    best_move = 0.3  # Move right more aggressively

        # Combine base steering with item-based adjustment
        steering += best_move

        #acceleration = max(0.1, 1 - abs(curvature) + max(0, slope))
        acceleration = 0.3
        nitro_threshold = 0.02
        use_nitro = abs(curvature) < nitro_threshold
        drift_threshold = 40
        use_drift = abs(curvature) > drift_threshold

        # Track agent position for visualization
        agent_abs_pos = np.array(self.env.unwrapped.world.karts[0].location)
        self.agent_positions.append(agent_abs_pos)

        action = {
            "acceleration": np.clip(acceleration, 0.1, 1),
            "steer": np.clip(steering, -1, 1),
            "brake": False,
            "drift": use_drift,
            "nitro": use_nitro,
            "rescue": True,
            "fire": False,
        }
        return action

    def step(self):
        """Take a single step in the environment."""
        action = self.calculate_action()
        self.obs, _, done, _, _ = self.env.step(action)
        return done

    def run(self, steps=10000):
        """Run the agent for a fixed number of steps."""
        self.reset()
        for step in range(steps):
            done = self.step()
            yield self.obs
            if done:
                break
        self.env.close()
