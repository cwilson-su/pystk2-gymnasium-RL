import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils")))
from csvRW import setup_output, read_csv_data
from plot import plt_multi_agent_plot

# Define paths
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_csv_base"))
csv_file = setup_output("multi_AI_custom_ActionS.csv", output_directory=csv_base_dir)

graph_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_graph_base"))
os.makedirs(graph_folder, exist_ok=True)

# Run the test script to generate the CSV
test_script = os.path.join(os.path.dirname(__file__), "multi_AI_customActionS-CSV.py")
subprocess.run(["python3", test_script])

data_dict = read_csv_data(csv_file, is_multi_agent=True)

steps = {agent: list(range(len(data_dict["Reward"][agent]))) for agent in data_dict["Reward"].keys()}
rewards = data_dict.get("Reward", [])
positions = data_dict.get("Position", [])
distances = data_dict.get("Distance", [])
velocities = data_dict.get("Velocity", [])
# Plot reward vs step

plt_multi_agent_plot(steps, rewards, "Steps", "Reward", "Multi-Agent: Reward vs Steps",
                       os.path.join(graph_folder, "multi_AI_reward_graph.png"))

# Plot position vs step

plt_multi_agent_plot(steps, positions, "Steps", "Position", "Multi-Agent: Position vs Steps",
                       os.path.join(graph_folder, "multi_AI_position_graph.png"))

# Plot distance vs step

plt_multi_agent_plot(steps, distances, "Steps", "Distance", "Multi-Agent: Distance vs Steps",
                       os.path.join(graph_folder, "multi_AI_distance_graph.png"))

# Plot velocity vs step

plt_multi_agent_plot(steps, velocities, "Steps", "Velocity (m/s)", "Multi-Agent: Velocity vs Steps",
                       os.path.join(graph_folder, "multi_AI_velocity_graph.png"))
