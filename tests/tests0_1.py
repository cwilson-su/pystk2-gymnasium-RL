import gymnasium as gym
import numpy as np  # Import NumPy for array handling
from pystk2_gymnasium import AgentSpec
import os
import csv

# Set the output folder to the `tests` directory
output_folder = os.path.join(os.path.dirname(__file__), "tests_csv")

# Ensure the folder exists (it should already exist, but this ensures robustness)
os.makedirs(output_folder, exist_ok=True)

csv_file = os.path.join(output_folder, "test0_1_results.csv")

# Write column titles (only once at the start of the script)
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Step", "Reward", "Terminated", "Truncated", "Position", "Distance", "Velocity"])

# STK gymnasium uses one process
if __name__ == '__main__':
    # Create the environment with flattened observation/action spaces
    env = gym.make(
        "supertuxkart/flattened-v0",  # Flattened environment
        render_mode="human",         # Enable rendering for visualization
        agent=AgentSpec(use_ai=False),  # Custom agent with manual actions
        track="xr591"                # Custom track
    )

    ix = 0
    done = False

    # Reset the environment
    state, *_ = env.reset()

    while not done:
        ix += 1

        # Define custom actions
        action = {
            "continuous": np.array([1.0, -0.5]),  # Acceleration (1.0), Steer left (-0.5)
            "discrete": [0, 0, 0, 0, 1]           # No brake, no drift, no nitro, fire, rescue
        }

        # Step the environment with the custom action
        state, reward, terminated, truncated, info = env.step(action)

        # Extract position and distance from info
        position = info.get("position", "N/A")  # Default to "N/A" if not found
        distance = info.get("distance", "N/A")  # Default to "N/A" if not found
        
        velocity = info.get("velocity", [0.0, 0.0, 0.0])
        speed = (velocity[0]**2 + velocity[1]**2 + velocity[2]**2)**0.5

        # Write the data to the CSV file
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([ix, reward, terminated, truncated, position, distance, speed])

        # Check if the episode is done
        done = truncated or terminated

    env.close()
