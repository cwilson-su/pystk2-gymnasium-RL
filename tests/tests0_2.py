# 3 agents
# 3 karts
# custom action space
# custom track

# TEST FAILS---------------------------------

import gymnasium as gym
from pystk2_gymnasium import AgentSpec

if __name__ == '__main__':
    agents = [
        AgentSpec(name="AI Agent 1", use_ai=True),
        AgentSpec(name="AI Agent 2", use_ai=True),
        AgentSpec(name="Human Agent", use_ai=False)
    ]

    # Create the environment for multiple agents
    env = gym.make(
        "supertuxkart/full-v0",
        render_mode="human",
        num_kart=3,
        track="xr591",  # Custom track
        laps=3,
        difficulty=1         # Medium difficulty
    )

    state, *_ = env.reset()
    done = False

    while not done:
        actions = {
            agent.name: {
                "steer": 0.5,
                "acceleration": 1.0,
                "brake": 0,
                "drift": 0,
                "fire": 0,
                "nitro": 1,
                "rescue": 1
            }
            for agent in agents
        }
        state, reward, terminated, truncated, _ = env.step(actions)
        done = terminated or truncated

    env.close()


