"""from StayInMiddleAgent import StayInMiddleAgent

if __name__ == "__main__":
    # Initialize the agent and specify the track
    # agent = StayInMiddleAgent(track="lighthouse", render_mode="human") #lighthouse is a really tough track
    agent = StayInMiddleAgent(track=None, render_mode="human")

    # Run the agent
    agent.run()
"""
from StayInTheMiddleAgentNoComputing import StayInMiddleAgentNoComputing

if __name__ == "__main__":
    agent = StayInMiddleAgentNoComputing(track=None, render_mode="human")

    # Ensure the agent runs by consuming the generator
    for obs in agent.run():
        pass  # You can print obs if needed: print(obs)
