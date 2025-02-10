import csv
import sys
import os
import subprocess
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common import setup_output, read_csv_data, plot_graph

# Define paths
test_script = os.path.join("tests", "refrac00.py")
csv_file = setup_output("test0_0_results.csv")
graph_folder = os.path.join("tests", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Execute the test script to generate the CSV files
subprocess.run(["python3", test_script])

# Read CSV data, taking into account the "Truncated" column if present
steps, rewards, positions, distances, velocities = read_csv_data(csv_file, has_truncated=True) 

# Correct negative velocity values
velocities = [max(0, v) for v in velocities]  

# Generate graphs
plot_graph(steps, rewards, "Steps", "Reward", "Test 0: Reward vs Steps", 
           os.path.join(graph_folder, "test0_0_reward_graph.png"))
plot_graph(steps, positions, "Steps", "Position", "Test 0: Position vs Steps", 
           os.path.join(graph_folder, "test0_0_position_graph.png"), color="green")
plot_graph(steps, distances, "Steps", "Distance", "Test 0: Distance vs Steps", 
           os.path.join(graph_folder, "test0_0_distance_graph.png"), color="purple")
plot_graph(steps, velocities, "Steps", "Velocity (m/s)", "Test 0: Velocity vs Steps", 
           os.path.join(graph_folder, "test0_0_velocity_graph.png"), color="orange")
