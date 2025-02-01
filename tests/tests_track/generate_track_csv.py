import csv
import os
import numpy as np
import gymnasium as gym
from pystk2_gymnasium import AgentSpec

''' Go check the self.obs keys in StayInMiddleAgent.py to understand the data structure. 
    It contains some hidden gems data the tracks ;)'''

'''
dict_keys(['phase', 'aux_ticks', 'powerup', 'attachment', 'attachment_time_left', 'max_steer_angle', 'energy', 
'skeed_factor', 'shield_time', 'jumping', 'distance_down_track', 'velocity', 'front', 'center_path_distance', 
'center_path', 'items_position', 'items_type', 'karts_position', 'paths_distance', 'paths_width', 'paths_start', 'paths_end'])
'''

# Function to generate track data and save to CSV
def generate_track_csv(track_name, output_file):
    
    agent = AgentSpec(name="Player", use_ai=True)
    env = gym.make("supertuxkart/full-v0", render_mode="human", agent=agent, track=track_name)
    obs, _ = env.reset()

    # Open CSV file for writing
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Center_X", "Center_Y", "Center_Z", "Left_X", "Left_Y", "Left_Z", "Right_X", "Right_Y", "Right_Z"])

        # Iterate through ALL track points
        for i in range(len(obs["paths_start"])):
            center_vector = np.array(obs["paths_start"][i])  # Use paths_start instead of static center
            track_width = obs["paths_width"][i][0]  # Extract track width value

            # Calculate left and right boundaries using directional estimation
            direction_vector = np.array(obs["paths_end"][i]) - np.array(obs["paths_start"][i])
            direction_vector = direction_vector / np.linalg.norm(direction_vector)  # Normalize direction

            # Compute perpendicular vector (approximate left/right direction)
            left_offset = np.cross(direction_vector, [0, 1, 0]) * (track_width / 2)
            right_offset = -left_offset

            left_vector = center_vector + left_offset
            right_vector = center_vector + right_offset

            writer.writerow([*center_vector, *left_vector, *right_vector])

    env.close()
    print(f"✅ Track data saved to {output_file}")

import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # I'm saving in the script's directory, but that can be changed later ofc
csv_path = os.path.join(current_dir, "track_data.csv")
generate_track_csv("xr591", csv_path)
