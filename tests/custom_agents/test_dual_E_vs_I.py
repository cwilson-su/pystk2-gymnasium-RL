#!/usr/bin/env python3
"""
Duel: EulerAgent versus ItemsAgent

Agent 0 is an EulerAgent (wrapping a fresh MedianAgent), and Agent 1 is an ItemsAgent
(which decorates an EulerAgent that itself wraps a MedianAgent). Both are set as human-controlled.
The simulation runs on the "black_forest" track with 2 karts.
"""

import sys, os
import numpy as np

# Append the "src" folder to sys.path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from customAgents.ItemsAgent import ItemsAgent
from pystk2_gymnasium.envs import STKRaceMultiEnv, AgentSpec

# Make AgentSpec hashable.
def agent_spec_hash(self):
    return hash((self.rank_start, self.use_ai, self.name, self.camera_mode))
AgentSpec.__hash__ = agent_spec_hash

# Create two agent specifications.
agents_specs = [
    AgentSpec(name="Euler", rank_start=0, use_ai=False),   # For the EulerAgent
    AgentSpec(name="Items", rank_start=1, use_ai=False)      # For the ItemsAgent
]

# Create the multi-agent environment for 2 karts.
env = STKRaceMultiEnv(agents=agents_specs, track="black_forest", render_mode="human", num_kart=3)

# Instantiate the agents.
# Agent 0: EulerAgent wraps a fresh MedianAgent.
euler_agent = EulerAgent(MedianAgent(env, path_lookahead=3))
# Agent 1: ItemsAgent wraps an EulerAgent that itself wraps a fresh MedianAgent.
items_agent = ItemsAgent(EulerAgent(MedianAgent(env, path_lookahead=3)))

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        actions = {}
        # Use keys "0" and "1" corresponding to the two agents.
        actions["0"] = euler_agent.calculate_action(obs["0"])
        actions["1"] = items_agent.calculate_action(obs["1"])
        obs, reward, done, truncated, info = env.step(actions)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
