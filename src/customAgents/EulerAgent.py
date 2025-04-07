import numpy as np
from utils.TrackUtils import compute_slope

class EulerAgent:
    def __init__(self, env, path_lookahead=3):
        self.env = env
        self.path_lookahead = path_lookahead
        self.agent_positions = []

    def euler_spiral_curvature(self, path_ends):
        if len(path_ends) < 3:
            return 0.01
        p1 = np.array(path_ends[0])
        p2 = np.array(path_ends[len(path_ends) // 2])
        p3 = np.array(path_ends[-1])
        v1 = p2 - p1
        v2 = p3 - p2
        # Calculer l'angle entre v1 et v2 en utilisant la norme du produit vectoriel
        cross_norm = np.linalg.norm(np.cross(v1, v2))
        dot_product = np.dot(v1, v2)
        angle = np.arctan2(cross_norm, dot_product)
        distance = np.linalg.norm(v1) + np.linalg.norm(v2)
        curvature = abs(angle) / max(distance, 1e-6)
        curvature = np.clip(curvature * 2.0, 0.01, 1.0)
        return curvature

    def calculate_action(self, obs):
        path_ends = obs["paths_end"][:self.path_lookahead]
        path_end = path_ends[-1]
        kart_front = obs["front"]

        curvature = float(self.euler_spiral_curvature(path_ends))
        slope = float(compute_slope(path_ends[:2]))

        acceleration = max(0.5, 1 - abs(curvature) + max(0, slope))
        direction_to_target = path_end - kart_front
        steering = 0.4 * direction_to_target[0] / (1.0 + abs(curvature) * 0.5)
        use_nitro = abs(curvature) < 0.05

        return {
            "acceleration": np.clip(acceleration, 0.5, 1),
            "steer": np.clip(steering, -1, 1),
            "brake": False,
            "drift": False,
            "nitro": use_nitro,
            "rescue": True,
            "fire": False
        }
