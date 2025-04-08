#!/usr/bin/env python3
"""
Test script for the basic MedianAgent on the 'black_forest' track.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.MedianAgent import MedianAgent
from pystk2_gymnasium.envs import STKRaceEnv, AgentSpec

agent_spec = AgentSpec(name="Median", rank_start=0, use_ai=False)
env = STKRaceEnv(agent=agent_spec, track="black_forest", render_mode="human")
median_agent = MedianAgent(env, path_lookahead=3)

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        action = median_agent.calculate_action(obs)
        obs, reward, done, truncated, info = env.step(action)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
