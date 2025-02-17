import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv


class FollowTrackNodesAgent:
    """Agent that attempts to follow all the nodes of the track."""
    def __init__(self, track, render_mode=None, num_kart=2):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.obs = None
        self.track_nodes = []
        self.current_node_index = 0

    def reset(self, track_nodes):
        """Resets the environment and sets the track nodes."""
        self.obs, _ = self.env.reset()
        self.track_nodes = track_nodes
        self.current_node_index = 0

    def calculate_action(self):
        """Compute the action to move toward the next node."""
        if self.current_node_index >= len(self.track_nodes):
            return {
                "acceleration": 0.0,  # Stop if no more nodes to follow
                "steer": 0.0,
                "brake": True,
                "drift": False,
                "nitro": False,
                "rescue": True,
                "fire": False,
            }

        # Current position of the kart
        kart_position = self.obs["center_path"]  # Use current position relative to path center

        print(self.obs["paths_start"])

        target_node = self.track_nodes[self.current_node_index]

        # Compute direction vector to the target node
        direction = np.array(target_node) - np.array(kart_position)
        distance_to_node = np.linalg.norm(direction)

        # Check if the target node is reached
        if distance_to_node < 2.0:  # Threshold for reaching a node
            self.current_node_index += 1  # Move to the next node
            return self.calculate_action()  # Recalculate action for the next node

        # Normalize the direction vector for steering
        normalized_direction = direction / max(distance_to_node, 1e-6)
        steering = -normalized_direction[0]  # X component determines left/right steering

        # Control logic for acceleration and steering
        action = {
            "acceleration": 0.5,  # Moderate acceleration
            "steer": np.clip(steering, -1, 1),  # Clip steering to valid range
            "brake": False,
            "drift": False,
            "nitro": False,
            "rescue": True,
            "fire": False,
        }
        return action

    def step(self):
        """Take a single step in the environment."""
        action = self.calculate_action()
        self.obs, _, done, _, _ = self.env.step(action)
        return done

    def run(self, track_nodes, steps=1000):
        """Run the agent for a fixed number of steps."""
        self.reset(track_nodes)
        for step in range(steps):
            done = self.step()
            if done:
                break

        self.env.close()
