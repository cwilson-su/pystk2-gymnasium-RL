import os
import csv
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define paths
test_script = os.path.join("tests", "tests0_3.py")
csv_file = os.path.join("tests", "tests_csv", "test0_3_results.csv")
track_nodes_file = os.path.join("tests", "tests_csv", "test0_3_track_nodes.csv")
graph_folder = os.path.join("tests", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Run the test script to generate the CSVs
subprocess.run(["python3", test_script])

# Read CSV data
steps = []
rewards = []
positions = []
distances = []
velocities = []

with open(csv_file, "r") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)  # Skip the header row
    for row in reader:
        steps.append(int(row[0]))          # Step
        rewards.append(float(row[1]))     # Reward
        positions.append(row[4])          # Position
        distances.append(float(row[5]))   # Distance
        velocities.append(float(row[6]))  # Velocity

# Plot reward vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, rewards, label="Reward", color="blue")
plt.xlabel("Steps")
plt.ylabel("Reward")
plt.title("Test 3: Reward vs Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_3_reward_graph.png"))
plt.show()

# Plot position vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, positions, label="Position", color="green")
plt.xlabel("Steps")
plt.ylabel("Position")
plt.title("Test 3: Position vs Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_3_position_graph.png"))
plt.show()

# Plot distance vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, distances, label="Distance", color="purple")
plt.xlabel("Steps")
plt.ylabel("Distance")
plt.title("Test 3: Distance vs Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_3_distance_graph.png"))
plt.show()

# Plot velocity vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, velocities, label="Velocity", color="orange")
plt.xlabel("Steps")
plt.ylabel("Velocity (m/s)")
plt.title("Test 3: Velocity vs Steps")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "test0_3_velocity_graph.png"))
plt.show()

# Plot track nodes in 3D
def plot_track_nodes(csv_file):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Read the track nodes from the CSV file
    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip the header row
        for row in reader:
            start = list(map(float, row[:3]))
            end = list(map(float, row[3:]))
            # Plot the segment
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color="blue")

    ax.set_title("Track Path Nodes", fontsize=16)
    ax.set_xlabel("X (Horizontal)")
    ax.set_ylabel("Y (Vertical)")
    ax.set_zlabel("Z (Depth)")
    plt.grid(True)
    plt.savefig(os.path.join(graph_folder, "test0_3_track_nodes_graph.png"))
    plt.show()

# Plot track nodes
plot_track_nodes(track_nodes_file)
