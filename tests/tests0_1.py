# 1 agent
# 5 karts
# custom action space
# no custom track
# no steer (and no other actions)

import gymnasium as gym
from pystk2_gymnasium import AgentSpec


if __name__ == '__main__':
    # Define a single agent (player-controlled)
    agent = AgentSpec(name="Player", use_ai=True)

    # !! Important note: Create the environment with at least two karts to prevent the karts_position list from being empty
    env = gym.make(
        "supertuxkart/full-v0",
        render_mode="human",
        num_kart=5,     #!!  Minimum of 2 karts to avoid empty karts_position
        # track="lighthouse",  # Custom track
        # track="snowtuxpeak",
        # track="zengarden",
        # track="minigolf",
        # track="sandtrack",
        # track="fortmagma",
        track="xr591",
        laps=3,
        difficulty=1    # Medium difficulty
    )

    state, *_ = env.reset()
    done = False

    while not done:
        # Define a sample action with default values
        action = {
            "steer": 0,           # Go straight
            "acceleration": 1.0,  # Full speed
            "brake": 0,           # No braking
            "drift": 0,           # No drifting
            "fire": 0,            # No item usage
            "nitro": 0,           # No nitro boost
            "rescue": 0           # No rescue
        }
        state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

    env.close()