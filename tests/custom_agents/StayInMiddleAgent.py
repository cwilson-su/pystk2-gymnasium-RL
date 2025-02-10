import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv

'''
I've tried to implement a simple agent that tries to stay in the middle of the track.
The initial idea was to do a simulation with 1 agent only, but the code is kinda 'hardcoded'to have a minimum of 2 karts on track.
I've tried to change the code to have only 1 kart, but I've faced some issues with sort_closest in envs.py, so I've decided to keep the code with 2 karts.
This class is also the first one I'm implementing which has a rescue mechanism from custom Saver script added to src

'''

class StayInMiddleAgent:
    """Agent that attempts to stay in the middle of the track."""
    def __init__(self, track, render_mode=None, num_kart=2):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.obs = None

    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()

    def calculate_action(self):
        """Compute the action to stay in the middle of the track."""
        center_distance = self.obs["center_path_distance"][0]  # Distance to center
        center_vector = self.obs["center_path"]  # Vector to the center

        # Steering adjustment based on the center vector's x-component
        steering = -0.05 * center_vector[0]

        # Simple control logic to accelerate and adjust steering
        action = {
            "acceleration": 0.075,  # If Input it at Full throttle, it goes off track more often
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
        return done

    """I've tried to make it run till 1 lap is completed, but idk where to find the info of the number of laps for now"""
    def run(self, steps=1000):
        """Run the agent for a fixed number of steps."""
        self.reset()
        for step in range(steps):
            done = self.step()
            yield self.obs
            if done:
                break

        self.env.close()
