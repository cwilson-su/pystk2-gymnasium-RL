import gymnasium as gym
import numpy as np
from followNthNextNode import FollowNthNextNode
from pystk2_gymnasium import AgentSpec

# Create the Agent
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

    # Initialize the agent with N=2 (follows second next node)
    follow_agent = FollowNthNextNode(env, n=3)

    while not done:
        step += 1

        # Compute the next action using our agent
        action = follow_agent.compute_action_space(states, infos)  # Now correctly passing both parameters

        # Step the environment
        states, reward, terminated, truncated, infos = env.step(action)

        done = terminated or truncated

    env.close()
