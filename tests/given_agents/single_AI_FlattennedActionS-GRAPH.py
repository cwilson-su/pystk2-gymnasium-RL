import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils")))
from csvRW import setup_output, read_csv_data
from plot import plt_plot

# Define paths
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv","given_agents"))
csv_file = setup_output("single_AI_Flattenned_ActionS.csv", output_directory=csv_base_dir)

# Run the test script to generate the CSV
test_script = os.path.join(os.path.dirname(__file__), "single_AI_FlattennedActionS-CSV.py")
subprocess.run(["python3", test_script])

# Read CSV data
#steps, rewards, terminated, truncated, positions, distances, velocities = read_csv_data(csv_file)
csv_data = read_csv_data(csv_file)
steps = csv_data["Step"]
rewards = csv_data["Reward"]
positions = csv_data["Position"]
distances = csv_data["Distance"]
velocities = csv_data["Velocity"]

# Define graph output folder
graph_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_graph","given_agents_visualizations"))
os.makedirs(graph_folder, exist_ok=True)

# Generate graphs
plt_plot(steps, rewards, "Steps", "Reward", "Single AI: Reward vs Steps",
        os.path.join(graph_folder, "single_AI_reward_graph.png"))

plt_plot(steps, positions, "Steps", "Position", "Single AI: Position vs Steps",
        os.path.join(graph_folder, "single_AI_position_graph.png"), color="green")

plt_plot(steps, distances, "Steps", "Distance", "Single AI: Distance vs Steps",
        os.path.join(graph_folder, "single_AI_distance_graph.png"), color="purple")

plt_plot(steps, velocities, "Steps", "Velocity (m/s)", "Single AI: Velocity vs Steps",
        os.path.join(graph_folder, "single_AI_velocity_graph.png"), color="orange")
