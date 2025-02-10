import csv
import sys
import os
import subprocess
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common import (
    setup_output, read_csv_data, plot_graph, plot_track_nodes
)

# Define paths
test_script = os.path.join("arc", "refrac03.py")
csv_file = setup_output("test0_3_results.csv")
track_nodes_file = setup_output("test0_3_track_nodes.csv")
graph_folder = os.path.join("arc", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Execute the test script to generate the CSV files
subprocess.run(["python3", test_script])

# Read CSV data, taking into account the "Truncated" column if present
steps, rewards, positions, distances, velocities = read_csv_data(csv_file, has_truncated=True)

# Correct negative velocity values
velocities = [max(0, v) for v in velocities]  

# Generate graphs
plot_graph(steps, rewards, "Steps", "Reward", "Test 3: Reward vs Steps", 
           os.path.join(graph_folder, "test0_3_reward_graph.png"))
plot_graph(steps, positions, "Steps", "Position", "Test 3: Position vs Steps", 
           os.path.join(graph_folder, "test0_3_position_graph.png"), color="green")
plot_graph(steps, distances, "Steps", "Distance", "Test 3: Distance vs Steps", 
           os.path.join(graph_folder, "test0_3_distance_graph.png"), color="purple")
plot_graph(steps, velocities, "Steps", "Velocity (m/s)", "Test 3: Velocity vs Steps", 
           os.path.join(graph_folder, "test0_3_velocity_graph.png"), color="orange")

# Generate the 3D graph of track nodes
plot_track_nodes(track_nodes_file, os.path.join(graph_folder, "test0_3_track_nodes_graph.png"))
