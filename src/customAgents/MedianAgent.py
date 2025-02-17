import numpy as np
from pystk2_gymnasium.envs import STKRaceEnv
import sys
import os
import csv
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.TrackUtils import compute_curvature, compute_slope, TrackVisualizer

class MedianAgent:
    """Agent that attempts to stay in the middle of the track using paths_end as the target."""
    def __init__(self, track, render_mode=None, num_kart=2, path_lookahead=3, plot=False):
        self.env = STKRaceEnv(track=track, render_mode=render_mode, num_kart=num_kart)
        self.path_lookahead = path_lookahead
        self.plot = plot
        self.obs = None
        self.agent_positions = []

    def reset(self):
        """Resets the environment and obtains the initial observation."""
        self.obs, _ = self.env.reset()
        self.agent_positions = []  

    def calculate_action(self):
        """Compute the action to stay on track using paths_end as the target."""
        if self.obs is None:
            return {}
        
        path_end = self.obs["paths_end"][self.path_lookahead - 1]
        kart_front = self.obs["front"]  # Direction the kart is facing

        path_ends = self.obs["paths_end"][:self.path_lookahead]
        curvature = compute_curvature(path_ends)  # Compute curvature based on path endpoints
        slope = compute_slope(path_ends[:2])  # Compute slope using first two path nodes
        
        # Compute the steering angle based on the direction to the path end
        direction_to_target = path_end - kart_front
        steering = 0.2 * direction_to_target[0]  # Using x-component to adjust steering

        acceleration = max(0.1, 1 - abs(curvature) + max(0, slope))  # Increase acceleration with positive upward slope
        nitro_threshold = 0.02  # Define curvature threshold for nitro activation
        use_nitro = abs(curvature) < nitro_threshold  # Use nitro if curvature is below threshold
        drift_threshold = 40  # Define curvature threshold for drift activation
        use_drift = abs(curvature) > drift_threshold  # Enable drift if curvature is high

        # Store agent position
        agent_abs_pos = np.array(self.env.unwrapped.world.karts[0].location)
        self.agent_positions.append(agent_abs_pos)

        # Simple control logic to accelerate and adjust steering
        action = {
            "acceleration": np.clip(acceleration, 0.1, 1),  # Adjusted acceleration
            "steer": np.clip(steering, -1, 1),  # Limit steering to [-1, 1]
            "brake": False,
            "drift": use_drift,  # Enable drift when curvature is high
            "nitro": use_nitro,  # Use nitro when in straight lines
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
        
        # If plotting is enabled, generate the graph
        if self.plot:
            self.generate_plot()

    def generate_plot(self):
        """Generate a plot of the agent's path using TrackVisualizer, including track and node data."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))  # Go to project root

        output_folder = os.path.join(project_root, "tests", "records_csv", "agent_path")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "agent_path.csv")

        # Write agent path to CSV
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Agent_X", "Agent_Y", "Agent_Z"])
            writer.writerows(self.agent_positions)

        # Load track and agent path data
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
