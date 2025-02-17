from StayInMiddleAgent import StayInMiddleAgent
from pystk2_gymnasium import AgentSpec
import gymnasium as gym
import numpy as np
import csv
import os
from utils.TrackUtils import compute_angle_beta
from StayInTheMiddleAgentNoComputing import StayInMiddleAgentNoComputing
from utils.csvRW import write_csv_header, write_to_csv


# Define the output folder and file
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "records_csv","beta_angle"))
os.makedirs(output_folder, exist_ok=True)
angle_csv_file = os.path.join(output_folder, "angle_beta_results.csv")
vectors_csv_file = os.path.join(output_folder, "vectors_log.csv")

# Write headers only once
write_csv_header(angle_csv_file, "Step", "Beta (degrees)")
write_csv_header(vectors_csv_file, "Step", "Velocity_X", "Velocity_Y", "Velocity_Z", "CenterPath_X", "CenterPath_Y", "CenterPath_Z")
    

if __name__ == "__main__":
    # Initialize the agent and specify the track

    #custom agent
    agent = StayInMiddleAgentNoComputing(track="lighthouse", render_mode="human")

    
    #ai agent
    '''
    agent = AgentSpec(name="Player", use_ai=True)
    env = gym.make("supertuxkart/full-v0", 
                render_mode="human", 
                agent=agent,
                track="lighthouse")
    '''
    
    #comment from here to use the custom agent code
    '''
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
        write_to_csv(angle_csv_file, step, beta)
        
        # Save velocity and center vectors to CSV
        write_to_csv(vectors_csv_file, step, *velocity, *center_vector)
        
        done = truncated or terminated
    '''
    
    # Uncomment to run the custom agent

    step = 0
    for obs in agent.run():  # Assuming agent.run() yields observations
        step += 1
        velocity = obs.get("velocity", np.array([0, 0, 0]))
        center_vector = obs.get("center_path", np.array([0, 0, 0]))
        beta = compute_angle_beta(velocity, center_vector)
        
       # Save angle beta to CSV
        write_to_csv(angle_csv_file, step, beta)
                
        # Save velocity and center vectors to CSV
        write_to_csv(vectors_csv_file, step, *velocity, *center_vector)
    
    
