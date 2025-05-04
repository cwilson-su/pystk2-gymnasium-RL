import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
import os
import csv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "utils"))) # Add src/utils to Python path
from csvRW import setup_output, write_csv_header, write_to_csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from customAgents.ItemsAgent import ItemsAgent
from pystk2_gymnasium.envs import STKRaceMultiEnv, AgentSpec

# Define correct directories
csv_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv","given_agents"))
csv_file = setup_output("E_vs_I.csv", output_directory=csv_base_dir)
csv_file_Track_Name = setup_output("Track_Name.csv", output_directory=csv_base_dir)

# Write column titles (only once at the start of the script)
write_csv_header(csv_file, "Agent", "Reward", "Terminated", "Position", "Distance", "Velocity")
write_csv_header(csv_file_Track_Name, "Track_Name")

#AgentSpec(name="Euler", rank_start=0, use_ai=False),   # For the EulerAgent
#AgentSpec(name="Items", rank_start=1, use_ai=False),      # For the ItemsAgent
#AgentSpec(name="Items1", rank_start=2, use_ai=False),     # For the ItemsAgent1
#AgentSpec(name="Median", rank_start=3, use_ai=False),

if __name__ == '__main__':
    # Create 5 agent specifications.
    agents_specs = [
        AgentSpec(name="Euler", rank_start=0, use_ai=False),   # For the EulerAgent
        AgentSpec(name="Items", rank_start=1, use_ai=False),      # For the ItemsAgent
    ]

    # Create the multi-agent environment for N karts.
    env = STKRaceMultiEnv(agents=agents_specs, track="fortmagma", render_mode="human", num_kart=2, difficulty=1)

    # Instantiate the agents.
    # Agent 0: EulerAgent wraps a fresh MedianAgent.
    euler_agent = EulerAgent(MedianAgent(env, path_lookahead=2))
    # Agent 1,2: ItemsAgent wraps an EulerAgent that itself wraps a fresh MedianAgent.
    items_agent = ItemsAgent(EulerAgent(MedianAgent(env, path_lookahead=2)))
    items_agent1 = ItemsAgent(MedianAgent(env, path_lookahead=2))
    # Agent 3: plain MedianAgent.
    median_agent = MedianAgent(env, path_lookahead=2)
    ix = 0
    done = False

    # Reset the environment
    obs, _ = env.reset()
    write_to_csv(csv_file_Track_Name, env.current_track)

    print("Track Name:", env.current_track)

    while not done and ix < 1000:
        ix += 1
        print("Step:", ix)

        #actions["0"] = euler_agent.calculate_action(obs["0"])
        #actions["1"] = items_agent.calculate_action(obs["1"])
        #actions["2"] = items_agent1.calculate_action(obs["2"])
        #actions["3"] = median_agent.calculate_action(obs["3"])
        
        actions = {}
        actions["0"] = euler_agent.calculate_action(obs["0"])
        actions["1"] = items_agent.calculate_action(obs["1"])

        # Step the environment with actions
        obs, reward, terminated, truncated, info = env.step(actions)

        # Log rewards and state info for each agent
        for i in range(len(agents_specs)):
            agent_reward = reward if isinstance(reward, (int, float)) else reward.get(str(i), 0.0)
            is_terminated = terminated.get(str(i), False) if isinstance(terminated, dict) else terminated
            agent_info = info['infos'].get(str(i), {}) if 'infos' in info and isinstance(info['infos'], dict) else {}
            velocity = obs[str(i)]["velocity"] if str(i) in obs else [0, 0, 0]
            speed = np.linalg.norm(velocity)
            position = agent_info.get("position", "N/A")
            distance = agent_info.get("distance", "N/A")
            write_to_csv(csv_file, i, agent_reward, is_terminated, position, distance, speed)
        # Check if all agents are done
        done = all(terminated.values()) if isinstance(terminated, dict) else terminated

    env.close()
