import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.TrackUtils import compute_curvature, compute_slope  

class MedianAgent:
    """Agent that attempts to stay in the middle of the track using paths_end as the target."""
    def __init__(self, track, render_mode=None, num_kart=2, path_lookahead=3):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.path_lookahead = path_lookahead
        self.obs = None
        self.agent_positions = []  # Keep recording positions for testing purposes

    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def calculate_action(self):
        """Compute the action to stay on track using paths_end as the target."""
        if self.obs is None:
            return {}
        
        path_end = self.obs["paths_end"][self.path_lookahead - 1]
        kart_front = self.obs["front"]

        path_ends = self.obs["paths_end"][:self.path_lookahead]
        curvature = compute_curvature(path_ends)
        slope = compute_slope(path_ends[:2])
        
        direction_to_target = path_end - kart_front
        steering = 0.2 * direction_to_target[0]

        acceleration = max(0.1, 1 - abs(curvature) + max(0, slope))
        nitro_threshold = 0.02
        use_nitro = abs(curvature) < nitro_threshold
        drift_threshold = 40
        use_drift = abs(curvature) > drift_threshold

        # Track agent position for testing visualization
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
