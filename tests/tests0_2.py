import gymnasium as gym
import numpy as np
from pystk2_gymnasium import AgentSpec

if __name__ == '__main__':
    # Define the specifications for 5 agents
    agents = [
        AgentSpec(use_ai=True, name="AI Agent 1"),       # AI-controlled agent
        AgentSpec(use_ai=True, name="Manual Agent 1"),  # Custom action agent       #-------/!\
        AgentSpec(use_ai=True, name="AI Agent 2"),       # AI-controlled agent
        AgentSpec(use_ai=True, name="Manual Agent 2"),  # Custom action agent       #-------/!\
        AgentSpec(use_ai=True, name="AI Agent 3"),       # AI-controlled agent
    ]

    # Create the environment for multiple agents
    env = gym.make(
        "supertuxkart/multi-full-v0",  # Multi-agent environment
        render_mode="human",          # Enable rendering for visualization
        agents=agents,                # Pass agent specifications
        track=None,                   # Use a random track
        num_kart=5,                   # Total number of karts
        laps=1,                       # Number of laps
        difficulty=2                  # AI difficulty level
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
                "steer": 0.0,      # No steering
                "acceleration": 1.0 if not agent.use_ai else 0.0,  # Full acceleration for manual agents
                "brake": False,       # No brake
                "drift": False,       # No drift
                "fire": False,        # No firing
                "nitro": False,       # No nitro boost
                "rescue": False,      # No rescue
            }

        # Step the environment with actions
        states, reward, terminated, truncated, info = env.step(actions)

        # Log rewards and state info for each agent
        for i in range(len(agents)):
            agent_reward = reward if isinstance(reward, (int, float)) else reward.get(str(i), 0.0)
            is_terminated = terminated.get(str(i), False) if isinstance(terminated, dict) else terminated
            agent_info = info['infos'].get(str(i), {}) if 'infos' in info and isinstance(info['infos'], dict) else {}
            print(
                f"Agent {i}: Reward={agent_reward}, "
                f"Terminated={is_terminated}, Info={agent_info}"
            )

        # Check if all agents are done
        done = all(terminated.values()) if isinstance(terminated, dict) else terminated

    # Stop the STK process to release resources
    env.close()


