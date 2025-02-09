import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
from common import (
    setup_output, write_csv_header, create_agent, initialize_environment,
    extract_data, write_to_csv
)

# Set up CSV file
csv_file = setup_output("test0_1_results.csv")

# Write CSV headers
write_csv_header(csv_file, ["Step", "Reward", "Terminated", "Position", "Distance", "Velocity"])

if __name__ == '__main__':
    # Initialize agent and environment
    agent = create_agent(name="Player", use_ai=False)
    env = initialize_environment(
        single_player=True, render_mode="human", agent=agent,
        track="xr591", laps=3, difficulty=2
    )

    step = 0
    done = False
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

        # Extract velocity, position, and distance
        speed, position, distance = extract_data(states, info)

        # Write to CSV
        write_to_csv(csv_file, [step, reward, terminated, position, distance, speed])

        # Check if race is done
        done = terminated or truncated

    env.close()
