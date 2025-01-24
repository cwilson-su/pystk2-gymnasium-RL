import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
import os
import csv

# Set the output folder for CSV
output_folder = os.path.join(os.path.dirname(__file__), "tests_csv")
os.makedirs(output_folder, exist_ok=True)

csv_file = os.path.join(output_folder, "test0_1_results.csv")

# Write CSV headers
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Step", "Reward", "Terminated", "Position", "Distance", "Velocity"])

if __name__ == '__main__':
    # Define a single agent (player-controlled)
    agent = AgentSpec(name="Player", use_ai=False)

    # Create the environment
    env = gym.make(
        "supertuxkart/full-v0",  # Single-agent environment
        render_mode="human",
        agent=agent,
        track="xr591",  # Custom track
        laps=3,
        difficulty=2
    )

    step = 0
    done = False

    # Reset the environment
    states, infos = env.reset()

    while not done:
        step += 1

        # Define a sample action for the agent
        action = {
            "steer": 0.0,
            "acceleration": 1.0,  # Full acceleration
            "brake": False,
            "drift": False,
            "fire": False,
            "nitro": False,
            "rescue": False
        }

        # Step the environment
        states, reward, terminated, truncated, info = env.step(action)

        # Extract velocity
        velocity = states["velocity"] if "velocity" in states else [0, 0, 0]
        speed = np.linalg.norm(velocity)

        # Extract position and distance
        position = info.get("position", "N/A")
        distance = info.get("distance", "N/A")

        # Write to CSV
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([step, reward, terminated, position, distance, speed])

        # Check if race is done
        done = terminated or truncated

    env.close()
