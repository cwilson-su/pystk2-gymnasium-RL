import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
from common import (
    setup_output, write_csv_header, create_agent, initialize_environment,
    extract_data, write_to_csv
)

# Set up CSV file
csv_file = setup_output("test0_0_results.csv")
write_csv_header(csv_file, ["Step", "Reward", "Terminated", "Truncated", "Position", "Distance", "Velocity"])

if __name__ == '__main__':
    # Initialize agent and environment
    agent = create_agent(name="Player", use_ai=False)
    env = initialize_environment(single_player=True, render_mode="human", agent=agent)
    
    ix = 0
    done = False
    states, infos = env.reset()

    while not done:
        ix += 1
        action = env.action_space.sample()
        states, reward, terminated, truncated, info = env.step(action)

        speed, position, distance = extract_data(states, info)
        write_to_csv(csv_file, [ix, reward, terminated, truncated, position, distance, speed])

        done = truncated or terminated

    env.close()
