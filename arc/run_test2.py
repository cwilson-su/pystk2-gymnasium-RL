import os
import csv
import subprocess
import matplotlib.pyplot as plt

# Define paths
test_script = os.path.join("tests", "tests0_2.py")
csv_file = os.path.join("tests", "tests_csv", "test0_2_results.csv")

# Run the test script
subprocess.run(["python3", test_script])

# Read CSV data
steps = {}
rewards = {}
positions = {}
distances = {}
velocities= {}

with open(csv_file, "r") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)  # Skip the header row
    for row in reader:
        agent = int(row[0])
        step = len(steps.get(agent, [])) + 1
        steps.setdefault(agent, []).append(step)
        rewards.setdefault(agent, []).append(float(row[1]))
        positions.setdefault(agent, []).append(row[3])  
        distances.setdefault(agent, []).append(float(row[4]))
        velocities.setdefault(agent, []).append(float(row[5]))

# Plot reward vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, rewards[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.title("Test 2: Reward vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_2_reward_graph.png"))
plt.show()

# Plot position vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, positions[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Position")
plt.title("Test 2: Position vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_2_position_graph.png"))
plt.show()

# Plot distance vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, distances[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Distance")
plt.title("Test 2: Distance vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_2_distance_graph.png"))
plt.show()


# Plot speed(velocity) vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, velocities[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Speed")
plt.title("Test 2: Speed vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_2_velocity_graph.png"))
plt.show()

