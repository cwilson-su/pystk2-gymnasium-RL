import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Set the output folder to the `tests` directory
output_folder = os.path.join(os.path.dirname(__file__), "tests_csv")

# Ensure the folder exists
os.makedirs(output_folder, exist_ok=True)

csv_file = os.path.join(output_folder, "test0_4_results.csv")

# Write column titles (only once at the start of the script)
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Agent", "Reward", "Terminated", "Position", "Distance", "Velocity"])

if __name__ == '__main__':
    # Define the specifications for 5 agents
    agents = [
        AgentSpec(use_ai=True, name="AI Agent 1"),  # AI-controlled agent
        AgentSpec(use_ai=True, name="Manual Agent 1"),  # Custom action agent
        AgentSpec(use_ai=True, name="AI Agent 2"),  # AI-controlled agent
        AgentSpec(use_ai=True, name="Manual Agent 2"),  # Custom action agent
        AgentSpec(use_ai=True, name="AI Agent 3"),  # AI-controlled agent
    ]

    # Create the environment for multiple agents
    env = gym.make(
        "supertuxkart/multi-full-v0",  # Multi-agent environment
        render_mode="human",          # Enable rendering for visualization
        agents=agents,                # Pass agent specifications
        track=None,                   # Use a random track
        num_kart=5,                   # Total number of karts
        laps=1,                       # Number of laps
        difficulty=2                  # AI difficulty level
    )

    done = False

    # Reset the environment
    states, infos = env.reset()

    while not done:
        actions = {}

        # Define actions for all agents
        for i, agent in enumerate(agents):
            actions[str(i)] = {
                "steer": 0.0,      # No steering
                "acceleration": 1.0 if not agent.use_ai else 0.0,  # Full acceleration for manual agents
                "brake": False,       # No brake
                "drift": False,       # No drift
                "fire": False,        # No firing
                "nitro": False,       # No nitro boost
                "rescue": False,      # No rescue
            }

        # Step the environment with actions
        states, reward, terminated, truncated, info = env.step(actions)

        # Log rewards and state info for each agent
        for i in range(len(agents)):
            agent_reward = reward.get(str(i), 0.0) if isinstance(reward, dict) else reward
            is_terminated = terminated.get(str(i), False) if isinstance(terminated, dict) else terminated
            agent_info = info['infos'].get(str(i), {}) if 'infos' in info and isinstance(info['infos'], dict) else {}

            # Extract velocity
            velocity = states[str(i)]["velocity"] if str(i) in states else [0, 0, 0]
            speed = np.linalg.norm(velocity)  # Compute the magnitude of velocity

            with open(csv_file, "a", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                position = agent_info.get("position", "N/A")  # Default to "N/A" if not found
                distance = agent_info.get("distance", "N/A")  # Default to "N/A" if not found
                writer.writerow([i, agent_reward, is_terminated, position, distance, speed])

        # Check if all agents are done
        done = all(terminated.values()) if isinstance(terminated, dict) else terminated

    env.close()

    # =========================
    # Plotting the Velocity Data
    # =========================

    # Load the CSV file
    data = pd.read_csv(csv_file, delimiter=";")

    # Initialize the plot
    plt.figure(figsize=(12, 8))

    # Iterate over each agent and plot their velocity
    for agent_id in range(5):  # Assuming agent IDs are 0 to 4
        agent_data = data[data["Agent"] == agent_id]
        plt.plot(
            agent_data.index,
            agent_data["Velocity"],
            label=f"Agent {agent_id}"
        )

    # Customize the plot
    plt.xlabel("Steps")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs. Steps for All Agents")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join("tests", "tests_graphs", "test1_Velocity.png"))


