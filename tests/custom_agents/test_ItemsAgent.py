#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

from pystk2_gymnasium.envs import STKRaceEnv, AgentSpec
from utils.ItemObservationWrapper import ItemObservationWrapper
from customAgents.ItemsAgent import ItemsAgent  

def main():
    agent_spec = AgentSpec(name="ItemsExpert", rank_start=0, use_ai=False)
    env = STKRaceEnv(agent=agent_spec, track=None, render_mode="human")
    env = ItemObservationWrapper(env)
    items_agent = ItemsAgent(env, path_lookahead=3)
    items_agent.reset()
    done = False
    step = 0
    while not done:
        done = items_agent.step()
        #print(f"Step {step} completed.")
        step += 1
        env.render()
    env.close()

if __name__ == "__main__":
    main()
