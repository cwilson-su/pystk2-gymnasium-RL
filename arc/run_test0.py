import os
import csv
import subprocess
import matplotlib.pyplot as plt

# Define paths
test_script = os.path.join("tests", "tests0_0.py")
csv_file = os.path.join("tests", "tests_csv", "test0_0_results.csv")

# Run the test script
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
        velocities.append(float(row[6])) 

# Plot reward vs step
plt.figure()
plt.plot(steps, rewards, label="Reward")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.title("Test 0: Reward vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_0_reward_graph.png"))
plt.show()

# Plot position vs step
plt.figure()
plt.plot(steps, positions, label="Position")
plt.xlabel("Step")
plt.ylabel("Position")
plt.title("Test 0: Position vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_0_position_graph.png"))
plt.show()

# Plot distance vs step
plt.figure()
plt.plot(steps, distances, label="Distance")
plt.xlabel("Step")
plt.ylabel("Distance")
plt.title("Test 0: Distance vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_0_distance_graph.png"))
plt.show()

# Plot velocity vs step
plt.figure()
plt.plot(steps, velocities, label="Velocity", color="orange")
plt.xlabel("Step")
plt.ylabel("Velocity (m/s)")
plt.title("Test 0: Velocity vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_0_velocity_graph.png"))
plt.show()
