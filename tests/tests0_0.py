# -----------------------This is the sample test that was given on the GitHub-------------------------

# 1 agent
# 1 kart
# flattened action space
# no custom track

import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
import os
import csv

# Set the output folder to the `tests` directory
output_folder = os.path.join(os.path.dirname(__file__), "tests_csv")

# Ensure the folder exists (it should already exist, but this ensures robustness)
os.makedirs(output_folder, exist_ok=True)

csv_file = os.path.join(output_folder, "test0_0_results.csv")

# Write column titles (only once at the start of the script)
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Step", "Reward", "Terminated", "Truncated", "Position", "Distance", "Velocity"])

# STK gymnasium uses one process
if __name__ == '__main__':
    # Use a flattened version of the observation and action spaces
    env = gym.make("supertuxkart/flattened-v0", render_mode="human", agent=AgentSpec(use_ai=True))

    ix = 0
    done = False
    state, *_ = env.reset()

    while not done:
        ix += 1
        action = env.action_space.sample()
        state, reward, terminated, truncated, info = env.step(action)

        # Extract position and distance directly from info
        position = info.get("position", "N/A")  # Default to "N/A" if not found
        distance = info.get("distance", "N/A")  # Default to "N/A" if not found
        
        velocity = state["kart"]["velocity"]  # Extract velocity from the state
        speed = np.linalg.norm(velocity)  # Compute the magnitude of velocity



        # Write the data to the CSV file
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")    # We chose the ";" as delimiter and not the "," since some of our team members use "," as decimal separator (french)
            writer.writerow([ix, reward, terminated, truncated, position, distance, speed])

        done = truncated or terminated

    env.close()
