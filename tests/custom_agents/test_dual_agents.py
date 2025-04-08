#!/usr/bin/env python3
"""
Test script for dual agents in a multi-agent environment.
For example, MedianAgent on one kart and ItemsAgent (decorating EulerAgent) on the other.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from customAgents.ItemsAgent import ItemsAgent
from pystk2_gymnasium.envs import STKRaceMultiEnv, AgentSpec
import numpy as np

# Patch for AgentSpec if necessary
def agent_spec_hash(self):
    return hash((self.rank_start, self.use_ai, self.name, self.camera_mode))
AgentSpec.__hash__ = agent_spec_hash

# Create two agent specifications.
agents_specs = [
    AgentSpec(name="Median", rank_start=1, use_ai=False),
    AgentSpec(name="ItemsExpert", rank_start=2, use_ai=False)
]

# Create the multi-agent environment.
env = STKRaceMultiEnv(agents=agents_specs, track="black_forest", render_mode="human")

# Instantiate agents: one as a plain MedianAgent, the other as ItemsAgent decorating EulerAgent.
median_agent = MedianAgent(env, path_lookahead=3)
euler_agent = EulerAgent(MedianAgent(env, path_lookahead=3))  # or directly wrap the median agent
items_agent = ItemsAgent(euler_agent)

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        actions = {}
        # Assume observation keys "0" and "1" correspond to the two agents.
        actions["0"] = median_agent.calculate_action(obs["0"])
        actions["1"] = items_agent.calculate_action(obs["1"])
        obs, reward, done, truncated, info = env.step(actions)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
