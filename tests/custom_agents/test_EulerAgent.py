#!/usr/bin/env python3
"""
Test script for EulerAgent in a solo race on the specified track.
EulerAgent decorates a MedianAgent.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from pystk2_gymnasium.envs import STKRaceEnv, AgentSpec

agent_spec = AgentSpec(name="Euler", rank_start=0, use_ai=False)
env = STKRaceEnv(agent=agent_spec, track="black_forest", render_mode="human")
# Create a base MedianAgent and then wrap it with EulerAgent.
base_agent = MedianAgent(env, path_lookahead=3)
euler_agent = EulerAgent(base_agent)

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        action = euler_agent.calculate_action(obs)
        obs, reward, done, truncated, info = env.step(action)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
