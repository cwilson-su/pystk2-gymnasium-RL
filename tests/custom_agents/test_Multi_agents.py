#!/usr/bin/env python3
"""
Test script for a multi-agent simulation with three agents:
 - Agent 0: MedianAgent (plain)
 - Agent 1: EulerAgent (wrapping a MedianAgent)
 - Agent 2: ItemsAgent (wrapping an EulerAgent which itself wraps a MedianAgent)

The simulation uses the STKRaceMultiEnv environment on the "black_forest" track.
"""

import sys, os
import numpy as np

# Append the "src" folder to the sys.path to import your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from customAgents.ItemsAgent import ItemsAgent
from pystk2_gymnasium.envs import STKRaceMultiEnv, AgentSpec

# Patch AgentSpec to make it hashable (needed by STKRaceMultiEnv)
def agent_spec_hash(self):
    return hash((self.rank_start, self.use_ai, self.name, self.camera_mode))
AgentSpec.__hash__ = agent_spec_hash

# Create three agent specifications with different starting positions.
agents_specs = [
    AgentSpec(name="Median", rank_start=0, use_ai=False),
    AgentSpec(name="Euler",  rank_start=1, use_ai=False),
    AgentSpec(name="Items",  rank_start=2, use_ai=False)
]

# Create the multi-agent environment on the "black_forest" track in "human" render mode.
env = STKRaceMultiEnv(agents=agents_specs, track="black_forest", render_mode="human")

# Instantiate the agents:
# - Agent 0 uses a plain MedianAgent.
median_agent = MedianAgent(env, path_lookahead=3)
# - Agent 1 is an EulerAgent that wraps a MedianAgent.
euler_agent = EulerAgent(MedianAgent(env, path_lookahead=3))
# - Agent 2 is an ItemsAgent that wraps an EulerAgent (which itself wraps a MedianAgent).
items_agent = ItemsAgent(EulerAgent(MedianAgent(env, path_lookahead=3)))

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        actions = {}
        # The environment returns a dictionary where keys "0", "1", "2" correspond to the agents
        actions["0"] = median_agent.calculate_action(obs["0"])
        actions["1"] = euler_agent.calculate_action(obs["1"])
        actions["2"] = items_agent.calculate_action(obs["2"])
        obs, reward, done, truncated, info = env.step(actions)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
