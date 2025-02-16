import pandas as pd
import plotly.graph_objects as go
import os
from utils.csvRW import CSVFileManager

class TrackVisualizer:
    def __init__(self, track_data, agent_path=None, nodes=None):
        """Handles visualization using Plotly."""
        self.track_data = track_data
        self.agent_path = agent_path if agent_path else []  # Handle None case
        self.nodes = nodes if nodes else []  # Handle None case

    def plot_track(self):
        """Generate a 3D visualization of the track, nodes, and agent path."""
        fig = go.Figure()

        # Track lines
        if self.track_data:
            fig.add_trace(go.Scatter3d(x=self.track_data['Center_X'], y=self.track_data['Center_Y'], z=self.track_data['Center_Z'],
                                       mode='lines', name='Center Line', line=dict(color='blue')))
            fig.add_trace(go.Scatter3d(x=self.track_data['Left_X'], y=self.track_data['Left_Y'], z=self.track_data['Left_Z'],
                                       mode='lines', name='Left Boundary', line=dict(color='red')))
            fig.add_trace(go.Scatter3d(x=self.track_data['Right_X'], y=self.track_data['Right_Y'], z=self.track_data['Right_Z'],
                                       mode='lines', name='Right Boundary', line=dict(color='green')))

        # Agent Path
        if self.agent_path:
            agent_x, agent_y, agent_z = zip(*self.agent_path)
            fig.add_trace(go.Scatter3d(x=agent_x, y=agent_y, z=agent_z,
                                       mode='lines', name='Agent Path', line=dict(color='orange', width=5)))

        # Nodes
        if self.nodes:
            node_x, node_y, node_z = zip(*self.nodes)
            fig.add_trace(go.Scatter3d(x=node_x, y=node_y, z=node_z,
                                       mode='markers', name='Track Nodes', marker=dict(size=2, color='purple')))

        # Layout
        fig.update_layout(
            title='3D Track, Nodes & Agent Path',
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            margin=dict(l=0, r=0, b=0, t=40)
        )

        fig.show()


class TrackDataLoader:
    """Loads track, nodes, and agent path data from CSV files."""
    
    @staticmethod
    def load_data(track_name):
        """Loads track boundaries, nodes, and agent path."""

        # Get file paths
        track_data_file = CSVFileManager.get_file_path(track_name, "track_data")
        track_nodes_file = CSVFileManager.get_file_path(track_name, "track_nodes")
        agent_path_file = CSVFileManager.get_file_path(track_name, "agent_path")

        # Load track data
        track_data = None
        if os.path.exists(track_data_file):
            df_track = pd.read_csv(track_data_file)
            track_data = {
                "Center_X": df_track["Center_X"],
                "Center_Y": df_track["Center_Y"],
                "Center_Z": df_track["Center_Z"],
                "Left_X": df_track["Left_X"],
                "Left_Y": df_track["Left_Y"],
                "Left_Z": df_track["Left_Z"],
                "Right_X": df_track["Right_X"],
                "Right_Y": df_track["Right_Y"],
                "Right_Z": df_track["Right_Z"]
            }

        # Load nodes
        nodes = None
        if os.path.exists(track_nodes_file):
            df_nodes = pd.read_csv(track_nodes_file)
            nodes = list(zip(df_nodes["Start_X"], df_nodes["Start_Y"], df_nodes["Start_Z"]))

        # Load agent path
        agent_positions = None
        if os.path.exists(agent_path_file):
            df_agent = pd.read_csv(agent_path_file)
            agent_positions = list(zip(df_agent["Agent_X"], df_agent["Agent_Y"], df_agent["Agent_Z"]))

        return track_data, agent_positions, nodes





import numpy as np

def compute_curvature(nodes):
    """
    Compute the curvature of a segment of track using centerline nodes.
    Curvature is estimated based on angle differences between consecutive nodes.
    """
    if nodes is None or len(nodes) < 3:
        print("Not enough nodes to compute curvature!") 
        return 0  # Not enough points to compute curvature
    
    print("Hello from compute_curvature function")
    
    nodes = np.asarray(nodes)

    direction_changes = []
    for i in range(len(nodes) - 1):
        dx = nodes[i + 1][0] - nodes[i][0]  # Extract X
        dy = nodes[i + 1][1] - nodes[i][1]  # Extract Y
        angle = np.arctan2(dy, dx)
        direction_changes.append(angle)

    if len(direction_changes) > 1:
        curvature = np.mean(np.diff(direction_changes)) * 10  # Increase sensitivity by scaling
    else:
        curvature = 0

    print(f"Computed Curvature: {curvature}")  
    return curvature





'''

def compute_curvature(nodes):
    """
    Compute curvature using three consecutive nodes in local coordinates.
    """
    if nodes is None or len(nodes) < 3:
        return 0  # Not enough points to compute curvature

    # Convert nodes into NumPy arrays
    try:
        p1 = np.array(nodes[0])[:2]  # Extract only X, Y
        p2 = np.array(nodes[len(nodes) // 2])[:2]
        p3 = np.array(nodes[-1])[:2]

        # Compute curvature as 1 / radius of the circle formed by three points
        A = np.array([
            [p1[0], p1[1], 1],
            [p2[0], p2[1], 1],
            [p3[0], p3[1], 1]
        ])
        B = np.array([
            [- (p1[0]**2 + p1[1]**2)],
            [- (p2[0]**2 + p2[1]**2)],
            [- (p3[0]**2 + p3[1]**2)]
        ])

        X = np.linalg.solve(A, B)
        xc, yc = -0.5 * X[0, 0], -0.5 * X[1, 0]
        radius = np.sqrt(xc**2 + yc**2 - X[2, 0])

        return 1 / radius if radius != 0 else 0

    except (np.linalg.LinAlgError, IndexError, ValueError):
        return 0  # If any error occurs, return zero curvature
'''





