import csv
import sys
import os
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common import setup_output, read_csv_data, plot_graph

# Define paths
test_script = os.path.join("tests", "refrac01.py")
csv_file = setup_output("test0_1_results.csv")
graph_folder = os.path.join("tests", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Run the test script
subprocess.run(["python3", test_script])

# Read CSV data
steps, rewards, positions, distances, velocities = read_csv_data(csv_file)

# Generate and save plots
plot_graph(steps, rewards, "Steps", "Reward", "Test 1: Reward vs Steps", os.path.join(graph_folder, "test0_1_reward_graph.png"))
plot_graph(steps, positions, "Steps", "Position", "Test 1: Position vs Steps", os.path.join(graph_folder, "test0_1_position_graph.png"), color="green")
plot_graph(steps, distances, "Steps", "Distance", "Test 1: Distance vs Steps", os.path.join(graph_folder, "test0_1_distance_graph.png"), color="purple")
plot_graph(steps, velocities, "Steps", "Velocity (m/s)", "Test 1: Velocity vs Steps", os.path.join(graph_folder, "test0_1_velocity_graph.png"), color="orange")
