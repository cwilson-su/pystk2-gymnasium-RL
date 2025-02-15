import csv
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from FollowTrackNodesAgent import FollowTrackNodesAgent


def load_track_nodes(csv_file):
    """Load track nodes from a CSV file."""
    track_nodes = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)  # Skip the header row
        for row in reader:
            start = list(map(float, row[:3]))
            track_nodes.append(start)  # Use only the start node for simplicity
    return track_nodes


def plot_track_and_agent(track_nodes, agent_positions):
    """
    Plot the real track nodes and the agent's visited nodes in a 3D graph.

    :param track_nodes: List of real track nodes (x, y, z).
    :param agent_positions: List of agent-visited positions (x, y, z).
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the real track nodes
    track_x, track_y, track_z = zip(*track_nodes)
    ax.plot(track_x, track_y, track_z, label="Track Nodes", color="blue", linewidth=2)

    # Plot the agent's visited positions
    agent_x, agent_y, agent_z = zip(*agent_positions)
    ax.plot(agent_x, agent_y, agent_z, label="Agent Path", color="red", linestyle="--", linewidth=2)

    # Configure the plot
    ax.set_title("Track Nodes vs. Agent Path", fontsize=16)
    ax.set_xlabel("X (Horizontal)")
    ax.set_ylabel("Y (Vertical)")
    ax.set_zlabel("Z (Depth)")
    ax.legend()
    plt.grid(True)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # Load the track nodes from the CSV file generated in tests0_3.py
    
    track_nodes_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv","track_nodes")), "test0_3_track_nodes.csv")
    track_nodes = load_track_nodes(track_nodes_file)

    # Initialize the agent and specify the track
    #agent = FollowTrackNodesAgent(track="xr591", render_mode="human")
    agent = FollowTrackNodesAgent(track=None, render_mode="human")

    # Run the agent and record its positions
    agent_positions = []

    def record_position():
        """Extract the agent's position from the observation."""
        return agent.obs["center_path"].tolist()

    # Start the agent's run and record positions
    agent.reset(track_nodes)
    for step in range(1000):  # Arbitrary step limit
        agent_positions.append(record_position())  # Save agent position
        done = agent.step()
        if done:
            break

    # Plot the real track nodes and the agent's visited positions
    plot_track_and_agent(track_nodes, agent_positions)
