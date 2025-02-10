import os
import csv
import subprocess
import matplotlib.pyplot as plt

# Define paths
test_script = os.path.join("tests", "tests0_1.py")
csv_file = os.path.join("tests", "tests_csv", "test0_1_results.csv")
graph_folder = os.path.join("tests", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Run the test script to generate the CSV
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
        positions.append(row[3])          # Position
        distances.append(float(row[4]))   # Distance
        velocities.append(float(row[5]))  # Velocity

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
