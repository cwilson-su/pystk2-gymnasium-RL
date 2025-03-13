import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv
import sys
import os
from scipy.integrate import quad
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.TrackUtils import compute_slope  

class EulerAgent:
    """Agent that attempts to stay in the middle of the track using paths_end as the target."""
    def __init__(self, track, render_mode=None, num_kart=2, path_lookahead=3):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.path_lookahead = path_lookahead
        self.obs = None
        self.agent_positions = []  # Keep recording positions for testing purposes
        self.prev_steering = 0.0
        
    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def euler_spiral_curvature(self, path_ends):
        if len(path_ends) < 3:
            return 0

        # Calcul dynamique de la courbure
        p1, p2, p3 = path_ends[0], path_ends[len(path_ends)//2], path_ends[-1]
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p2)

        # Utilisation du produit vectoriel pour déterminer l'angle
        angle = np.arctan2(np.cross(v1, v2), np.dot(v1, v2))

        # Calcul de la courbure (1 / rayon du cercle osculateur)
        distance = np.linalg.norm(v1) + np.linalg.norm(v2)
        curvature = abs(angle) / distance

        # Option 1 : Transformer `curvature` en scalaire (recommandé si problème persistant)
        curvature = np.mean(curvature)

        return curvature * 2.0  # Facteur ajusté pour améliorer la stabilité



    def calculate_action(self):
        """Compute the action to stay on track using paths_end as the target."""
        if self.obs is None:
            return {}
        
        path_end = self.obs["paths_end"][self.path_lookahead - 1]
        kart_front = self.obs["front"]

        path_ends = self.obs["paths_end"][:self.path_lookahead]
        curvature = self.euler_spiral_curvature(path_ends)
        slope = compute_slope(path_ends[:2])
        
        direction_to_target = path_end - kart_front
        print(abs(curvature))
        # Zone morte pour stabiliser les lignes droites
        if abs(direction_to_target[0]) < 0.05:
            steering = 0.0
        else:
            # Steering contrôlé selon la courbure
            if abs(curvature) < 0.02:
                steering = 0.2 * direction_to_target[0]  # Faible steering en courbure légère
            else:
                steering = 3 * direction_to_target[0]  # Steering renforcé dans les virages serrés

        # Filtrage dynamique du steering
        #steering = 0.6 * self.prev_steering + 0.4 * steering
       # self.prev_steering = steering

        acceleration = 1.0 #max(0.1, 1 - abs(curvature) + max(0, slope))
        nitro_threshold = 0.02
        use_nitro = abs(curvature) < nitro_threshold
        drift_threshold = 40
        use_drift = abs(curvature) > drift_threshold

        agent_abs_pos = np.array(self.env.unwrapped.world.karts[0].location)
        self.agent_positions.append(agent_abs_pos)

        action = {
            "acceleration": 1.0, #np.clip(acceleration, 0.1, 1),
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
