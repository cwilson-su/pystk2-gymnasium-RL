import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from utils.TrackUtils import compute_curvature
from pystk2_gymnasium.envs import STKRaceEnv

class StayInMiddleAgent:
    """Agent that attempts to stay in the middle of the track using paths_end as the target."""
    def __init__(self, track, render_mode=None, num_kart=2):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.obs = None

    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()

    def calculate_action(self):
        """Compute the action to stay on track using paths_end as the target and adapt to curvature."""
        if self.obs is None:
            return {}
        
        path_ends = self.obs["paths_end"][:3]  # Get the next 3 path endpoints
        curvature = compute_curvature(path_ends)  # Compute curvature based on path endpoints

        print(curvature)
        
        path_end = path_ends[2]  # Use the first path end as the immediate target
        kart_front = self.obs["front"]  # Direction the kart is facing
        
        # Compute the steering angle based on the direction to the path end
        direction_to_target = path_end - kart_front
        steering = 0.1 * direction_to_target[0] * (1 + curvature)  # Adjust steering by curvature

        acceleration = max(0.1, 1 - abs(curvature))  # Min acceleration 0.05, reducing when curvature increases

        # Simple control logic to accelerate and adjust steering
        action = {
            "acceleration": acceleration,  # Adjusted acceleration
            "steer": np.clip(steering, -1, 1),  # Limit steering to [-1, 1]
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
        #print(self.obs)
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
