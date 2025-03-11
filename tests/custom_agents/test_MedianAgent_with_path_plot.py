import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.MedianAgent import MedianAgent
from utils.TrackPathWrapper import plot_agent_path_with_track



if __name__ == "__main__":
    agent = MedianAgent(track=None, render_mode="human")  # Removed `plot` argument

    # Run the agent to collect path data
    for obs in agent.run():
        pass  

    # Plot the collected path data using the wrapper
    plot_agent_path_with_track(agent, agent.env, "black_forest")
