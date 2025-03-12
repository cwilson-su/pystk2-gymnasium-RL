import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.ItemsAgent import ItemsAgent

if __name__ == "__main__":
    agent = ItemsAgent(track=None, render_mode="human")

    for obs in agent.run():
        pass
