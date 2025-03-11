import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.MedianAgent import MedianAgent


if __name__ == "__main__":
    agent = MedianAgent(track=None, render_mode="human") #by default, path_lookahead is 3
    
    # agent = MedianAgent(track=None, render_mode="human", path_lookahead=2) # min path_lookahead is 2
    
    # Ensure the agent runs by consuming the generator
    for obs in agent.run():
        pass  
