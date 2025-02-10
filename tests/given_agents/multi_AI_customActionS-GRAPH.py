import os
import csv
import subprocess
import matplotlib.pyplot as plt

# Define paths
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_csv_base"))
csv_file = os.path.join(csv_base_dir, "multi_AI_customActionS.csv")

graph_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_graph_base"))
os.makedirs(graph_folder, exist_ok=True)

# Run the test script to generate the CSV
test_script = os.path.join(os.path.dirname(__file__), "multi_AI_customActionS-CSV.py")
subprocess.run(["python3", test_script])

# Read CSV data
steps = {}
rewards = {}
positions = {}
distances = {}
velocities = {}

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
plt.title("Multi-Agent: Reward vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "multi_AI_reward_graph.png"))
plt.show()

# Plot position vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, positions[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Position")
plt.title("Multi-Agent: Position vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "multi_AI_position_graph.png"))
plt.show()

# Plot distance vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, distances[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Distance")
plt.title("Multi-Agent: Distance vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "multi_AI_distance_graph.png"))
plt.show()

# Plot velocity vs step
plt.figure()
for agent, agent_steps in steps.items():
    plt.plot(agent_steps, velocities[agent], label=f"Agent {agent}")
plt.xlabel("Step")
plt.ylabel("Speed")
plt.title("Multi-Agent: Speed vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(graph_folder, "multi_AI_velocity_graph.png"))
plt.show()
