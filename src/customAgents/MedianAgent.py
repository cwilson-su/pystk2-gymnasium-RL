import numpy as np
from utils.TrackUtils import compute_curvature, compute_slope

class MedianAgent:
    def __init__(self, env, path_lookahead=3):
        self.env = env
        self.path_lookahead = path_lookahead
        self.agent_positions = []

    def calculate_action(self, obs):
        path_ends = obs["paths_end"][:self.path_lookahead]
        path_end = path_ends[-1]
        kart_front = obs["front"]

        curvature = compute_curvature(path_ends)
        slope = compute_slope(path_ends[:2])

        direction_to_target = path_end - kart_front
        steering = 0.2 * direction_to_target[0]
        acceleration = max(0.5, 1 - abs(curvature) + max(0, slope))
        use_drift = abs(curvature) > 40
        use_nitro = abs(curvature) < 0.02

        return {
            "acceleration": np.clip(acceleration, 0.5, 1),
            "steer": np.clip(steering, -1, 1),
            "brake": False,
            "drift": use_drift,
            "nitro": use_nitro,
            "rescue": True,
            "fire": False
        }
