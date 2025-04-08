#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from pystk2_gymnasium.envs import STKRaceEnv, AgentSpec
from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from customAgents.ItemsAgent import ItemsAgent
from utils.ItemObservationWrapper import ItemObservationWrapper  

agent_spec = AgentSpec(name="ItemsExpert", rank_start=0, use_ai=False)
env = STKRaceEnv(agent=agent_spec, track=None, render_mode="human")
env = STKRaceEnv(agent=agent_spec, track=None, render_mode="human")
# Apply the custom observation wrapper to enrich item data.
env = ItemObservationWrapper(env)
# Create a base agent, wrap with EulerAgent, then wrap with ItemsAgent.
base_agent = MedianAgent(env, path_lookahead=3)
euler_agent = EulerAgent(base_agent)
items_agent = ItemsAgent(euler_agent)

def main():
    items_agent.reset()
    done = False
    step = 0
    while not done:
        done = items_agent.step()
        print(f"Step {step} completed.")
        step += 1
        env.render()
    env.close()

if __name__ == "__main__":
    main()
