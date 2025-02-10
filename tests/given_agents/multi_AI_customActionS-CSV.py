import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
import os
import csv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils"))) # Add src/utils to Python path
from csvRW import setup_output, write_csv_header, write_to_csv

# Define correct directories
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ZZ_csv_base"))
csv_file = setup_output("multi_AI_custom_ActionS.csv", output_directory=csv_base_dir)

# Write column titles (only once at the start of the script)
write_csv_header(csv_file, "Agent", "Reward", "Terminated", "Position", "Distance", "Velocity")

if __name__ == '__main__':
    # Define the specifications for 5 agents
    agents = [
        AgentSpec(use_ai=True, name="AI Agent 1"),
        AgentSpec(use_ai=True, name="Manual Agent 1"),
        AgentSpec(use_ai=True, name="AI Agent 2"),
        AgentSpec(use_ai=True, name="Manual Agent 2"),
        AgentSpec(use_ai=True, name="AI Agent 3"),
    ]

    # Create the environment for multiple agents
    env = gym.make(
        "supertuxkart/multi-full-v0",
        render_mode="human",
        agents=agents,
        track=None,
        num_kart=5,
        laps=1,
        difficulty=2
    )

    ix = 0
    done = False

    # Reset the environment
    states, infos = env.reset()

    while not done:
        ix += 1
        actions = {}

        # Define actions for all agents
        for i, agent in enumerate(agents):
            actions[str(i)] = {
                "steer": 0.0,
                "acceleration": 1.0 if not agent.use_ai else 0.0,
                "brake": False,
                "drift": False,
                "fire": False,
                "nitro": False,
                "rescue": False,
            }

        # Step the environment with actions
        states, reward, terminated, truncated, info = env.step(actions)

        # Log rewards and state info for each agent
        for i in range(len(agents)):
            agent_reward = reward if isinstance(reward, (int, float)) else reward.get(str(i), 0.0)
            is_terminated = terminated.get(str(i), False) if isinstance(terminated, dict) else terminated
            agent_info = info['infos'].get(str(i), {}) if 'infos' in info and isinstance(info['infos'], dict) else {}
            velocity = states[str(i)]["velocity"] if str(i) in states else [0, 0, 0]
            speed = np.linalg.norm(velocity)
            position = agent_info.get("position", "N/A")
            distance = agent_info.get("distance", "N/A")
            write_to_csv(csv_file, i, agent_reward, is_terminated, position, distance, speed)
        # Check if all agents are done
        done = all(terminated.values()) if isinstance(terminated, dict) else terminated

    env.close()
