import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils"))) # Add src/utils to Python path
from csvRW import setup_output, write_csv_header, write_to_csv 
import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec

# Set up CSV file
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_csv_base"))
csv_file = setup_output("single_AI_Flattenned_ActionS.csv", output_directory=csv_base_dir)
write_csv_header(csv_file, "Step", "Reward", "Terminated", "Truncated", "Position", "Distance", "Velocity")

if __name__ == '__main__':
    agent = AgentSpec(name="Player", use_ai=True)
    env = gym.make("supertuxkart/full-v0", render_mode="human", agent=agent)

    ix = 0
    done = False
    states, infos = env.reset()

    while not done:
        ix += 1
        action = env.action_space.sample()
        states, reward, terminated, truncated, info = env.step(action)
        
        speed = np.linalg.norm(states.get("velocity", [0, 0, 0]))
        position = info.get("position", "N/A")
        distance = info.get("distance", "N/A")
        
        write_to_csv(csv_file, ix, reward, terminated, truncated, position, distance, speed)

        done = truncated or terminated

    env.close()
