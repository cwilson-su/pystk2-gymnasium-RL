import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv
import sys
import os
import csv
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.TrackUtils import compute_curvature, compute_slope, compute_angle_beta, TrackVisualizer

class OptimizedMedianAgent:
    def __init__(self, track, render_mode=None, num_kart=2, path_lookahead=3, plot=False):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.path_lookahead = path_lookahead
        self.plot = plot
        self.obs = None
        self.agent_positions = []

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []  

    def euler_spiral_curvature(self, path_ends):
        if len(path_ends) < 3:
            return 0

        curvature = compute_curvature(path_ends)
        return curvature * 1.5

    def calculate_action(self):
        if self.obs is None:
            return {}
        
        path_end = self.obs["paths_end"][self.path_lookahead - 1]
        kart_front = self.obs["front"]

        path_ends = self.obs["paths_end"][:self.path_lookahead]
        curvature = self.euler_spiral_curvature(path_ends)
        #slope = compute_slope(path_ends[:2])
        #angle_beta = compute_angle_beta(self.obs["velocity"], self.obs["center_path"])
        
        direction_to_target = path_end - kart_front
        steering = 0.3 * direction_to_target[0]

        
        use_nitro = abs(curvature) < 0.5
        
        agent_abs_pos = np.array(self.env.unwrapped.world.karts[0].location)
        self.agent_positions.append(agent_abs_pos)

        action = {
            "acceleration": 1.0,
            "steer": np.clip(steering, -1, 1),
            "brake": False,
            "drift": False,
            "nitro": use_nitro,
            "rescue": True,
            "fire": False,
        }
        return action

    def step(self):
        action = self.calculate_action()
        self.obs, _, done, _, _ = self.env.step(action)
        return done

    def run(self, steps=10000):
        self.reset()
        for step in range(steps):
            done = self.step()
            yield self.obs
            if done:
                break

        self.env.close()
        
        if self.plot:
            self.generate_plot()

    def generate_plot(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        output_folder = os.path.join(project_root, "tests", "records_csv", "agent_path")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "agent_path.csv")

        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Agent_X", "Agent_Y", "Agent_Z"])
            writer.writerows(self.agent_positions)

        track_data_file = os.path.join(project_root, "tests", "records_csv", "track_data", "track_data.csv")
        track_nodes_file = os.path.join(project_root, "tests", "records_csv", "track_nodes", "track_nodes.csv")
        df_track = pd.read_csv(track_data_file)
        df_nodes = pd.read_csv(track_nodes_file)
        df_agent = pd.read_csv(output_file)

        track_data = {
            "Center_X": df_track["Center_X"],
            "Center_Y": df_track["Center_Y"],
            "Center_Z": df_track["Center_Z"],
            "Left_X": df_track["Left_X"],
            "Left_Y": df_track["Left_Y"],
            "Left_Z": df_track["Left_Z"],
            "Right_X": df_track["Right_X"],
            "Right_Y": df_track["Right_Y"],
            "Right_Z": df_track["Right_Z"]
        }

        nodes = list(zip(df_nodes["Start_X"], df_nodes["Start_Y"], df_nodes["Start_Z"]))
        agent_positions = list(zip(df_agent["Agent_X"], df_agent["Agent_Y"], df_agent["Agent_Z"]))

        visualizer = TrackVisualizer(track_data=track_data, agent_path=agent_positions, nodes=nodes)
        visualizer.plot_track()