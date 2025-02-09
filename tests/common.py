import os
import csv
import numpy as np
import gymnasium as gym
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pystk2_gymnasium import AgentSpec

def setup_output(csv_filename):
    """Creates the output directory and initializes a CSV file."""
    output_folder = os.path.join(os.path.dirname(__file__), "tests_csv")
    os.makedirs(output_folder, exist_ok=True)
    csv_file = os.path.join(output_folder, csv_filename)
    return csv_file

def write_csv_header(csv_file, headers):
    """Writes the header row to a CSV file."""
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)

def create_agent(name="Player", use_ai=False):
    """Creates an agent specification."""
    return AgentSpec(name=name, use_ai=use_ai)

def initialize_environment(single_player=True, **kwargs):
    """Initializes the SuperTuxKart environment."""
    if single_player:
        return gym.make("supertuxkart/full-v0", **kwargs)
    else:
        return gym.make("supertuxkart/multi-full-v0", **kwargs)


def extract_data(states, info):
    """Extracts relevant data such as velocity, position, and distance."""
    velocity = states.get("velocity", [0, 0, 0])
    speed = np.linalg.norm(velocity)

    # Vérification de la vitesse (éviter NaN, inf, ou None)
    if math.isnan(speed) or math.isinf(speed) or speed is None:
        speed = 0.0  # Remplace par une valeur sûre

    position = info.get("position", "N/A")
    distance = info.get("distance", "N/A")
    return speed, position, distance


def write_to_csv(csv_file, data):
    """Writes a row of data to a CSV file."""
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(data)

def save_track_nodes(env, track_nodes_file):
    """Saves track node information to a CSV file."""
    track = env.unwrapped.track
    with open(track_nodes_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Start_X", "Start_Y", "Start_Z", "End_X", "End_Y", "End_Z"])
        for segment in track.path_nodes:
            start, end = segment
            writer.writerow([*start, *end])

def read_csv_data(csv_file, has_agents=False, has_truncated=False):
    """Reads CSV data and returns structured information.

    """
    if has_agents:
        steps, rewards, positions, distances, velocities = {}, {}, {}, {}, {}
    else:
        steps, rewards, positions, distances, velocities = [], [], [], [], []

    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter=";")
        headers = next(reader)  

        for row in reader:
            expected_columns = 7 if has_truncated else 6 

            if len(row) < expected_columns:
                continue

            if has_agents:
                agent = int(row[0])
                step = len(steps.get(agent, [])) + 1
                steps.setdefault(agent, []).append(step)
                rewards.setdefault(agent, []).append(float(row[1]))
                positions.setdefault(agent, []).append(row[4 if has_truncated else 3])  
                distances.setdefault(agent, []).append(float(row[5 if has_truncated else 4]))
                velocities.setdefault(agent, []).append(float(row[6 if has_truncated else 5]))
            else:
                steps.append(int(row[0]))  # Step
                rewards.append(float(row[1]))  # Reward
                positions.append(row[4 if has_truncated else 3])  # Position
                distances.append(float(row[5 if has_truncated else 4]))  # Distance
                velocities.append(float(row[6 if has_truncated else 5]))  # Velocity

    return steps, rewards, positions, distances, velocities




def plot_graph(x_data, y_data, x_label, y_label, title, filename, color="blue"):
    """Generates and saves a plot."""
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, label=y_label, color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)

def plot_multi_agent_graph(steps_data, agent_data, x_label, y_label, title, filename):
    """Generates and saves a multi-agent plot where all agents' data are displayed on the same graph."""
    plt.figure(figsize=(10, 6))

    for agent in steps_data.keys():
        plt.plot(steps_data[agent], agent_data[agent], label=f"Agent {agent}")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)

def plot_track_nodes(csv_file, output_filename):
    """Generates and saves a 3D visualization of track path nodes."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Read the track nodes from the CSV file
    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip the header row
        for row in reader:
            start = list(map(float, row[:3]))
            end = list(map(float, row[3:]))
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color="blue")

    ax.set_title("Track Path Nodes", fontsize=16)
    ax.set_xlabel("X (Horizontal)")
    ax.set_ylabel("Y (Vertical)")
    ax.set_zlabel("Z (Depth)")
    plt.grid(True)
    plt.savefig(output_filename)