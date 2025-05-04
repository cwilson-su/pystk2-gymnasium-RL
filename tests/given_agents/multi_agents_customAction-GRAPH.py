import os
import sys
import subprocess
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils")))
from csvRW import setup_output, read_csv_data
from plot import plt_multi_agent_plot

# Define paths
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv","given_agents"))
csv_file = setup_output("multi_agents_custom_Action.csv", output_directory=csv_base_dir)
csv_file_Track_Name = setup_output("Track_Name.csv", output_directory=csv_base_dir)

graph_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_graph","given_agents_visualizations"))
os.makedirs(graph_folder, exist_ok=True)

# Run the test script to generate the CSV
test_script = os.path.join(os.path.dirname(__file__), "multi_agents_customAction-CSV.py")
subprocess.run(["python3", test_script])

data_dict = read_csv_data(csv_file, is_multi_agent=True)
data_dict_track = pd.read_csv(csv_file_Track_Name)
track_name = data_dict_track.iloc[0, 0]
print("Track Name:", track_name)

steps = {agent: list(range(len(data_dict["Reward"][agent]))) for agent in data_dict["Reward"].keys()}
rewards = data_dict.get("Reward", [])
positions = data_dict.get("Position", [])
distances = data_dict.get("Distance", [])
velocities = data_dict.get("Velocity", [])
# Plot reward vs step

plt_multi_agent_plot(steps, rewards, "Steps", "Reward", "Multi-Agent: Reward vs Steps",
                       os.path.join(graph_folder, f"{track_name}_multi_agents_reward_graph.png"))

# Plot position vs step

plt_multi_agent_plot(steps, positions, "Steps", "Position", "Multi-Agent: Position vs Steps",
                       os.path.join(graph_folder, f"{track_name}_multi_agents_position_graph.png"))

# Plot distance vs step

plt_multi_agent_plot(steps, distances, "Steps", "Distance", "Multi-Agent: Distance vs Steps",
                       os.path.join(graph_folder, f"{track_name}_multi_agents_distance_graph.png"))

# Plot velocity vs step

plt_multi_agent_plot(steps, velocities, "Steps", "Velocity (m/s)", "Multi-Agent: Velocity vs Steps",
                       os.path.join(graph_folder, f"{track_name}_multi_agents_velocity_graph.png"))
