import sys
import os
import subprocess

from matplotlib import pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils")))
from csvRW import setup_output, read_csv_data
from plot import plt_plot

# Define paths
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_csv_base"))
csv_file = setup_output("single_NoAI_customActionS.csv", output_directory=csv_base_dir)

# Run the test script to generate the CSV
test_script = os.path.join(os.path.dirname(__file__), "single_NoAI_customActionS-CSV.py")
subprocess.run(["python3", test_script])

# Read CSV data
csv_data = read_csv_data(csv_file)
steps, rewards, positions, distances, velocities = csv_data[0], csv_data[1], csv_data[-3], csv_data[-2], csv_data[-1]


# Define graph output folder
graph_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_graph_base"))
os.makedirs(graph_folder, exist_ok=True)


# Generate graphs
plt_plot(steps, rewards, "Steps", "Reward", "Single No AI: Reward vs Steps",
        os.path.join(graph_folder, "single_NoAI_reward_graph.png"))

plt_plot(steps, positions, "Steps", "Position", "Single No AI: Position vs Steps",
        os.path.join(graph_folder, "single_NoAI_position_graph.png"), color="green")

plt_plot(steps, distances, "Steps", "Distance", "Single No AI: Distance vs Steps",
        os.path.join(graph_folder, "single_NoAI_distance_graph.png"), color="purple")

plt_plot(steps, velocities, "Steps", "Velocity (m/s)", "Single No AI: Velocity vs Steps",
        os.path.join(graph_folder, "single_NoAI_velocity_graph.png"), color="orange")


'''
# Plot reward vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, rewards, label="Reward", color="blue")
plt.xlabel("Steps")
plt.ylabel("Reward")
plt.title("Reward vs. Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_1_reward_graph.png"))
plt.show()

# Plot position vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, positions, label="Position", color="green")
plt.xlabel("Steps")
plt.ylabel("Position")
plt.title("Position vs. Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_1_position_graph.png"))
plt.show()

# Plot distance vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, distances, label="Distance", color="purple")
plt.xlabel("Steps")
plt.ylabel("Distance")
plt.title("Distance vs. Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_1_distance_graph.png"))
plt.show()

# Plot velocity vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, velocities, label="Velocity", color="orange")
plt.xlabel("Steps")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity vs. Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_1_velocity_graph.png"))
plt.show()

'''
