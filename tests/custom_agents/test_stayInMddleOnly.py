from StayInMiddleAgent import StayInMiddleAgent

if __name__ == "__main__":
    # Initialize the agent and specify the track
    # agent = StayInMiddleAgent(track="lighthouse", render_mode="human") #lighthouse is a really tough track
    agent = StayInMiddleAgent(track=None, render_mode="human")

    # Run the agent
    agent.run()
