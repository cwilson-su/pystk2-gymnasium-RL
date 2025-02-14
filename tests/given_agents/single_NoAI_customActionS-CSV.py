import sys
import os
import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils"))) 
from csvRW import setup_output, write_csv_header, write_to_csv 

csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv","given_agents"))
csv_file = setup_output("single_NoAI_customActionS.csv", output_directory=csv_base_dir)

write_csv_header(csv_file, "Step", "Reward", "Terminated", "Position", "Distance", "Velocity")

if __name__ == '__main__':
    agent = AgentSpec(name="Player", use_ai=False)

    # Create the environment
    env = gym.make(
        "supertuxkart/full-v0", 
        render_mode="human",
        agent=agent,
        track="xr591",  
        laps=3,
        difficulty=2
    )

    step = 0
    done = False
    states, infos = env.reset()

    while not done:
        step += 1

        # Define a sample action for the agent
        action = {
            "steer": 0.0,
            "acceleration": 1.0,  
            "brake": False,
            "drift": False,
            "fire": False,
            "nitro": False,
            "rescue": False
        }

        # Step the environment
        states, reward, terminated, truncated, info = env.step(action)

        # Extract velocity, position, and distance
        speed = np.linalg.norm(states.get("velocity", [0, 0, 0]))
        position = info.get("position", "N/A")
        distance = info.get("distance", "N/A")

        # Write data to CSV
        write_to_csv(csv_file, step, reward, terminated, position, distance, speed)

        done = terminated or truncated

    env.close()
