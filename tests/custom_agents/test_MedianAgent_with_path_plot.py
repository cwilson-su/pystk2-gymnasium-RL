import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.MedianAgent import MedianAgent
from utils.TrackPathWrapper import plot_agent_path_with_track, plot_agent_path_with_items



if __name__ == "__main__":
    agent = MedianAgent(track=None, render_mode="human") 

    # Run the agent to collect path data
    for obs in agent.run():
        pass  

    plot_agent_path_with_track(agent, agent.env, "black_forest")
    
    #plot_agent_path_with_items(agent, agent.env, "black_forest")

