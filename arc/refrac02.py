import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec
from common import (
    setup_output, write_csv_header, create_agent, initialize_environment,
    extract_data, write_to_csv
)

# Set up CSV file
csv_file = setup_output("test0_2_results.csv")
write_csv_header(csv_file, ["Agent", "Reward", "Terminated", "Position", "Distance", "Velocity"])

if __name__ == '__main__':
    # Define agents
    agents = [
        create_agent(name="AI Agent 1", use_ai=True),
        create_agent(name="Manual Agent 1", use_ai=True),
        create_agent(name="AI Agent 2", use_ai=True),
        create_agent(name="Manual Agent 2", use_ai=True),
        create_agent(name="AI Agent 3", use_ai=True),
    ]
    
    # Initialize multi-agent environment
    env = initialize_environment(single_player=False, render_mode="human", agents=agents, track=None, num_kart=5, laps=1, difficulty=2)
    
    ix = 0
    done = False
    states, infos = env.reset()

    while not done:
        ix += 1
        actions = {str(i): {"steer": 0.0, "acceleration": 1.0 if not agent.use_ai else 0.0, "brake": False, "drift": False, "fire": False, "nitro": False, "rescue": False} for i, agent in enumerate(agents)}
        
        states, reward, terminated, truncated, info = env.step(actions)

        for i in range(len(agents)):
            agent_reward = reward.get(str(i), 0.0) if isinstance(reward, dict) else reward
            is_terminated = terminated.get(str(i), False) if isinstance(terminated, dict) else terminated
            agent_info = info['infos'].get(str(i), {}) if 'infos' in info else {}
            speed, position, distance = extract_data(states.get(str(i), {}), agent_info)
            write_to_csv(csv_file, [i, agent_reward, is_terminated, position, distance, speed])

        done = all(terminated.values()) if isinstance(terminated, dict) else terminated

    env.close()
