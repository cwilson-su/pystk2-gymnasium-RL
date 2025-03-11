import os
import os
import csv
import pandas as pd
import numpy as np
from utils.TrackUtils import TrackVisualizer

def plot_agent_path_with_track(agent, env, track_name):
    """
    Plots the track data and agent path using TrackVisualizer.
    Handles both custom and given agents.
    """

    # Define file paths
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    track_data_file = os.path.join(base_path, "records_csv", "track_data", f"{track_name}_track_data.csv")
    track_nodes_file = os.path.join(base_path, "records_csv", "track_nodes", f"{track_name}_track_nodes.csv")
    agent_path_file = os.path.join(base_path, "records_csv", "agent_path", f"{track_name}_agent_path.csv")

    # Ensure directories exist
    os.makedirs(os.path.dirname(track_data_file), exist_ok=True)
    os.makedirs(os.path.dirname(track_nodes_file), exist_ok=True)
    os.makedirs(os.path.dirname(agent_path_file), exist_ok=True)

    # Handle observation source based on agent type
    if hasattr(agent, 'obs'):  # Custom Agent (e.g., MedianAgent)
        obs = agent.obs
    else:  # Given Agent (e.g., AgentSpec)
        obs, _ = env.reset()

    # Save track data
    with open(track_data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Center_X", "Center_Y", "Center_Z", "Left_X", "Left_Y", "Left_Z", "Right_X", "Right_Y", "Right_Z"])
        for i in range(len(obs["paths_start"])):
            center_vector = np.array(env.unwrapped.track.path_nodes[i][0])
            track_width = obs["paths_width"][i][0]
            direction_vector = np.array(env.unwrapped.track.path_nodes[i][1]) - np.array(env.unwrapped.track.path_nodes[i][0])
            direction_vector = direction_vector / np.linalg.norm(direction_vector)
            left_offset = np.cross(direction_vector, [0, 1, 0]) * (track_width / 2)
            right_offset = -left_offset
            left_vector = center_vector + left_offset
            right_vector = center_vector + right_offset
            writer.writerow([*center_vector, *left_vector, *right_vector])

    # Save track nodes
    track = env.unwrapped.track
    with open(track_nodes_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Start_X", "Start_Y", "Start_Z", "End_X", "End_Y", "End_Z"])
        for segment in track.path_nodes:
            start, end = segment
            writer.writerow([*start, *end])

    # Save agent path using recorded positions
    with open(agent_path_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Agent_X", "Agent_Y", "Agent_Z"])
        if hasattr(agent, 'agent_positions'):  # Custom Agent (e.g., MedianAgent)
            writer.writerows(agent.agent_positions)
        else:  # Given Agent (e.g., AgentSpec) needs path tracking
            done = False
            agent_positions = []
            while not done:
                action = env.action_space.sample()
                obs, _, terminated, truncated, _ = env.step(action)
                agent_abs_pos = np.array(env.unwrapped.world.karts[0].location)
                agent_positions.append(agent_abs_pos)
                writer.writerow(agent_abs_pos)
                done = terminated or truncated

    # Load CSV data
    df_track = pd.read_csv(track_data_file)
    df_nodes = pd.read_csv(track_nodes_file)
    df_agent = pd.read_csv(agent_path_file)

    # Format data for visualization
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

    # Visualize
    visualizer = TrackVisualizer(track_data=track_data, agent_path=agent_positions, nodes=nodes)
    visualizer.plot_track()

