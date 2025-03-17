import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv
from scipy.integrate import quad
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.TrackUtils import compute_curvature, compute_slope  

class EulerAgent:
    """Optimized agent using Euler Spiral principles for improved cornering and speed management."""
    
    def __init__(self, track, render_mode=None, num_kart=2, path_lookahead=3):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.path_lookahead = path_lookahead
        self.obs = None
        self.agent_positions = []  

    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def euler_spiral_curvature(self, path_ends):
        """Calculates curvature using Euler Spiral principles for smoother trajectories."""
        if len(path_ends) < 3:
            return 0

        p1, p2, p3 = path_ends[0], path_ends[len(path_ends)//2], path_ends[-1]
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p2)

        angle = np.arctan2(np.cross(v1, v2), np.dot(v1, v2))
        distance = np.linalg.norm(v1) + np.linalg.norm(v2)
        curvature = abs(angle) / distance


        curvature = curvature * 2.0

        curvature = np.clip(curvature, 0.01, 1.0)

        return curvature

    def calculate_action(self):
        """Compute the action based on optimal racing line logic with Euler Spiral principles."""
        if self.obs is None:
            return {}

        path_end = self.obs["paths_end"][self.path_lookahead - 1]
        kart_front = self.obs["front"]

        path_ends = self.obs["paths_end"][:self.path_lookahead]
        curvature = self.euler_spiral_curvature(path_ends)
        slope = compute_slope(path_ends[:2])

        # Si curvature ou slope est un tableau, prendre la valeur maximale
        if isinstance(curvature, np.ndarray):
            curvature = np.max(curvature)
        if isinstance(slope, np.ndarray):
            slope = np.max(slope)

        # Correction de la logique d'accélération
        acceleration = max(0.5, 1 - abs(curvature) + max(0, slope))

        # Définition correcte du steering
        direction_to_target = path_end - kart_front
        steering = 0.4 * direction_to_target[0] / (1.0 + abs(curvature) * 0.5)

        # Nitro usage when curvature is low to maintain maximum speed
        nitro_threshold = 0.05
        use_nitro = abs(curvature) < nitro_threshold

        # Track agent position for visualization
        agent_abs_pos = np.array(self.env.unwrapped.world.karts[0].location)
        self.agent_positions.append(agent_abs_pos)

        action = {
            "acceleration": np.clip(acceleration, 0.5, 1),
            "steer": np.clip(steering, -1, 1),  # Steering correctement défini
            "brake": False,
            "drift": False,
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
