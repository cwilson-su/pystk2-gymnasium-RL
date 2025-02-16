import numpy as np
import pandas as pd
from utils.TrackUtils import compute_curvature

class AutoAgent:
    def __init__(self, lookahead=5):
        """AutoAgent makes decisions based on upcoming track curvature using relative positions."""
        self.lookahead = lookahead
        self.agent_path = []  # Store agent path dynamically
        self.obs = None  # Observation will be updated dynamically each step

    def update_observation(self, obs):
        """Update the agent's latest observation from the environment."""
        self.obs = obs


    '''
    def get_future_nodes(self):
        """Fetch the next available track nodes from obs['center_path'], up to the lookahead distance."""
        if self.obs is None or "center_path" not in self.obs or len(self.obs["center_path"]) < 3:
            return None  # Ensure at least 3 nodes exist

        nodes = np.array(self.obs["center_path"])  # Convert to NumPy array
        end_index = min(self.lookahead, len(nodes))  # Avoid out-of-bounds indexing
        nodes = nodes[:end_index]  # Get only the lookahead points

        # Ensure nodes has the correct shape
        if nodes.ndim == 1:  # If 1D, convert to at least (N, 3)
            nodes = np.expand_dims(nodes, axis=0)  

        return nodes if len(nodes) >= 3 else None  # Ensure at least 3 points
    
    '''
    def get_future_nodes(self):
        """Fetch multiple upcoming track nodes from obs['paths_start'] instead of obs['center_path']."""
        if self.obs is None:
            print("Error: self.obs is None!")
            return None

        if "paths_start" in self.obs and len(self.obs["paths_start"]) >= self.lookahead:
            nodes = np.array(self.obs["paths_start"])  # Convert to NumPy array
        else:
            print("Error: 'paths_start' key is missing in obs or too short!")
            return None

        end_index = min(self.lookahead, len(nodes))  # Ensure valid indexing
        future_nodes = nodes[:end_index]  # Extract lookahead nodes

        print(f"Extracted Future Nodes: {future_nodes}")  # Debugging print
        return future_nodes

    


    def decide_action(self):
        """Decide acceleration, steering, braking, and drifting based on curvature analysis."""
        future_nodes = self.get_future_nodes()

        # Handle missing node data
        if future_nodes is None:
            print("Future nodes are None!")
            return {"steer": 0.0, "acceleration": 0.5, "brake": 1, "drift": 0, "fire": 0, "nitro": 0, "rescue": 0}

        curvature = compute_curvature(future_nodes)
        print(f"Computed Curvature: {curvature}")

        # Default action values
        action = {
            "steer": 0.0,
            "acceleration": 1.0,
            "brake": 0,
            "drift": 0,
            "fire": 0,
            "nitro": 0,
            "rescue": 0
    }

        # Define curvature thresholds
        STRAIGHT_THRESHOLD = 0.05  # Below this value, drive straight
        MAX_STEER = 0.6  # Prevent oversteering
        SCALE_FACTOR = 3.0  # Adjust steering sensitivity

        if abs(curvature) < STRAIGHT_THRESHOLD:
            print("Straight detected! Keeping steer = 0.0")
            action["steer"] = 0.0
        elif curvature > STRAIGHT_THRESHOLD:  # Right turn
            action["steer"] = min(MAX_STEER, curvature * SCALE_FACTOR)
            action["acceleration"] = max(0.7, 1.0 - curvature * 2)
            action["drift"] = 0.5  
        elif curvature < -STRAIGHT_THRESHOLD:  # Left turn
            action["steer"] = max(-MAX_STEER, curvature * SCALE_FACTOR)
            action["acceleration"] = max(0.7, 1.0 - abs(curvature) * 2)
            action["drift"] = 0.5  

        print(f"Final Action: {action}")
        return action


    def update_position(self, agent_pos):
        """Store agent path data for visualization."""
        self.agent_path.append(agent_pos)
        # print(self.obs)
        print(f"obs['center_path']: {self.obs.get('center_path', 'MISSING')}") 
