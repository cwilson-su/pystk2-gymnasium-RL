import csv
import sys
import os
import subprocess

from common import setup_output, read_csv_data, plot_multi_agent_graph


# Define paths
test_script = os.path.join("arc", "refrac02.py")
csv_file = setup_output("test0_2_results.csv")
graph_folder = os.path.join("arc", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Run the test script
subprocess.run(["python3", test_script])

# Read CSV data (multi-agent mode)
steps, rewards, positions, distances, velocities = read_csv_data(csv_file, has_agents=True)

# Generate and save combined plots for all agents with correct step mapping
plot_multi_agent_graph(steps, rewards, "Steps", "Reward", "Test 2: Reward vs Steps (All Agents)",
                       os.path.join(graph_folder, "test0_2_reward_graph.png"))

plot_multi_agent_graph(steps, positions, "Steps", "Position", "Test 2: Position vs Steps (All Agents)",
                       os.path.join(graph_folder, "test0_2_position_graph.png"))

plot_multi_agent_graph(steps, distances, "Steps", "Distance", "Test 2: Distance vs Steps (All Agents)",
                       os.path.join(graph_folder, "test0_2_distance_graph.png"))

plot_multi_agent_graph(steps, velocities, "Steps", "Velocity (m/s)", "Test 2: Velocity vs Steps (All Agents)",
                       os.path.join(graph_folder, "test0_2_velocity_graph.png"))
