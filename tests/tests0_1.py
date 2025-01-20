import gymnasium as gym
import numpy as np  # Import NumPy for array handling
from pystk2_gymnasium import AgentSpec

# STK gymnasium uses one process
if __name__ == '__main__':
    # Create the environment with flattened observation/action spaces
    env = gym.make(
        "supertuxkart/flattened-v0",  # Flattened environment
        render_mode="human",         # Enable rendering for visualization
        agent=AgentSpec(use_ai=False)  # Custom agent with manual actions
    )

    ix = 0
    done = False

    # Reset the environment
    state, *_ = env.reset()

    while not done:
        ix += 1

        # Define custom actions
        action = {
            "continuous": np.array([1.0, -0.5]),  # Acceleration (1.0), Steer left (-0.5)
            "discrete": [0, 0, 0, 0, 0]           # No brake, no drift, no nitro, etc.
        }

        # Step the environment with the custom action
        state, reward, terminated, truncated, _ = env.step(action)
        print(f"Step {ix}: Reward={reward}, Terminated={terminated}, Truncated={truncated}")
        
        # Check if the episode is done
        done = truncated or terminated

    # Stop the STK process to release resources
    env.close()