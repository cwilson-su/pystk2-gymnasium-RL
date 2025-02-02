from StayInMiddleAgent import StayInMiddleAgent
from pystk2_gymnasium import AgentSpec
import gymnasium as gym
import numpy as np
import csv
import os

# Define the output folder and file
output_folder = os.path.join(os.path.dirname(__file__), "tests_csv")
os.makedirs(output_folder, exist_ok=True)
angle_csv_file = os.path.join(output_folder, "angle_beta_results.csv")
vectors_csv_file = os.path.join(output_folder, "vectors_log.csv")
# Write column titles (only once at the start of the script)
with open(angle_csv_file, "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Step", "Beta (degrees)"])
    

if __name__ == "__main__":
    # Initialize the agent and specify the track

    #custom agent
    #agent = StayInMiddleAgent(track="lighthouse", render_mode="human")

    #ai agent
    agent = AgentSpec(name="Player", use_ai=True)
    env = gym.make("supertuxkart/full-v0", 
                render_mode="human", 
                agent=agent,
                track="lighthouse")

    # Function to compute angle beta between two vectors
    def compute_angle_beta(velocity, center_vector):
        if np.linalg.norm(velocity) == 0 or np.linalg.norm(center_vector) == 0:
            return None  # Avoid division by zero
        
        dot_product = np.dot(velocity, center_vector)
        magnitude_product = np.linalg.norm(velocity) * np.linalg.norm(center_vector)
        
        # Compute angle in radians
        beta_rad = np.arccos(np.clip(dot_product / magnitude_product, -1.0, 1.0))
        
        # Convert to degrees
        beta_deg = np.degrees(beta_rad)
        return beta_deg


    #comment from here to use the custom agent code
    ix = 0
    done = False
    states, infos = env.reset()
    
    while not done:
        ix += 1
        action = env.action_space.sample()
        states, reward, terminated, truncated, info = env.step(action)
        velocity = states["velocity"] if "velocity" in states else [0, 0, 0]
        center_vector = states["center_path"] if "center_path" in states else [0, 0, 0]
        beta = compute_angle_beta(velocity, center_vector)
        # Save angle beta to CSV
        with open(angle_csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([ix, beta])
        
        # Save velocity and center vectors to CSV
        with open(vectors_csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([ix, *velocity, *center_vector])
        
        done = truncated or terminated

    
    # Uncomment to run the custom agent
"""
    step = 0
    for obs in agent.run():  # Assuming agent.run() yields observations
        step += 1
        velocity = obs.get("velocity", np.array([0, 0, 0]))
        center_vector = obs.get("center_path", np.array([0, 0, 0]))
        beta = compute_angle_beta(velocity, center_vector)
        
        # Save angle beta to CSV
        with open(angle_csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([step, beta])
        
        # Save velocity and center vectors to CSV
        with open(vectors_csv_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([step, *velocity, *center_vector])
    """
    
