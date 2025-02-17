import sys
import os
import csv
import gymnasium as gym
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from pystk2_gymnasium import AgentSpec
from customAgents.AutoAgent import AutoAgent
from utils.TrackUtils import TrackVisualizer

# Define track name
track_name = "xr591"

# Define output directories
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv"))
agent_path_file = os.path.join(base_dir, f"{track_name}_agent_path.csv")

# Initialize environment
agent_spec = AgentSpec(name="Player", use_ai=False)
env = gym.make("supertuxkart/full-v0", render_mode="human", agent=agent_spec, track=track_name)
obs, _ = env.reset()

lookahead_value=3
print(f"Running simulation with lookahead = {lookahead_value}")
    
# Initialize AutoAgent
auto_agent = AutoAgent(lookahead=lookahead_value)

nodes = []  # Store node positions
track_nodes = env.unwrapped.track.path_nodes
nodes.extend(track_nodes)

# Track agent path
with open(agent_path_file.replace(".csv", f"_{lookahead_value}.csv"), "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Agent_X", "Agent_Y", "Agent_Z"])
    done = False

    
    while not done:
        auto_agent.update_observation(obs)
        action = auto_agent.decide_action()
        obs, _, terminated, truncated, _ = env.step(action)
        
        # Extract agent position
        agent_position = env.unwrapped.world.karts[0].location
        auto_agent.update_position(agent_position)
        writer.writerow(agent_position)

        done = terminated or truncated

# Load agent path
df_agent_path = pd.read_csv(agent_path_file.replace(".csv", f"_{lookahead_value}.csv"))
agent_positions = list(zip(df_agent_path['Agent_X'], df_agent_path['Agent_Y'], df_agent_path['Agent_Z']))

# Visualize everything
visualizer = TrackVisualizer(track_data=None, agent_path=agent_positions, nodes=nodes)
visualizer.plot_track()

env.close()
