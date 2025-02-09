import os
import csv
import numpy as np
import gymnasium as gym
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
