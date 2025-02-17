import numpy as np

class FollowNthNextNode:
    def __init__(self, env, n=2):
        """
        Initialize the agent to follow the Nth next node.
        
        :param env: The SuperTuxKart environment
        :param n: The number of nodes ahead to follow
        """
        self.env = env
        self.n = n
        self.nodes = np.array(self.env.unwrapped.track.path_nodes)  # Get track nodes at start

    def get_closest_node_index(self, kart_pos):
        """
        Finds the closest node to the current kart position.
        
        :param kart_pos: The position of the kart
        :return: Index of the closest node
        """
        distances = np.linalg.norm(self.nodes - kart_pos, axis=1)
        return np.argmin(distances)  # Index of the closest node

    def get_target_node(self, current_index):
        """
        Finds the N-th next node in the track.

        :param current_index: The index of the current closest node
        :return: The position of the N-th next node
        """
        target_index = (current_index + self.n) % len(self.nodes)  # Ensure circular track continuity
        return self.nodes[target_index]

    def compute_action_space(self, states, infos):
        """
        Computes the action space to steer towards the target node.
        
        :param states: The current state from env
        :param infos: Additional information from env
        :return: A dictionary with full action space
        """
        #kart_pos = np.array(self.env.unwrapped.world.karts[0].location)  # Get kart position
        #kart_front = np.array(self.env.unwrapped.world.karts[0].front)  # Get kart front direction

        print(f"Environment Type: {type(self.env)}")
        print(dir(self.env.wrapper_spec))  # Show all attributes and methods

        kart_pos = np.array(self.env.world.karts[0].location)  # Get kart position
        kart_front = np.array(self.env.world.karts[0].front)  # Get kart front direction

        

        # Find closest node and target node
        closest_node_index = self.get_closest_node_index(kart_pos)
        target_node = self.get_target_node(closest_node_index)

        # Compute direction vector to the target node
        direction_to_target = target_node - kart_pos

        # Compute angles
        target_angle = np.arctan2(direction_to_target[1], direction_to_target[0])  # Angle to target
        kart_angle = np.arctan2(kart_front[1], kart_front[0])  # Actual kart forward direction

        # Compute steering adjustment (normalize angle difference)
        #steering = (target_angle - kart_angle + np.pi) % (2 * np.pi) - np.pi  # Normalize angle to [-π, π]
        #steering = np.clip(angle_diff, -1, 1)  # Gain factor for smooth control
        steering = float(np.mean((target_angle - kart_angle + np.pi) % (2 * 1) - 1))*-1
        # **Ensure steering is a scalar value**
        #steering = float(np.mean(steering))  # Fix array issue

        # Define acceleration and braking logic
        distance_to_target = np.linalg.norm(direction_to_target)
        acceleration = 1.0 if distance_to_target > 2.0 else 0.5  # Slow down when close
        brake = 0.0 if acceleration > 0 else 1.0

        # Drift logic (activate only for sharp turns)
        drift = 1 if np.abs(steering) > 0.5 else 0

        # Nitro logic (use if distance to the target node is large)
        nitro = 1 if distance_to_target > 5.0 else 0

        # Fire (not needed, but can be set to 0 for completeness)
        fire = 0

        # Rescue (only if the kart is stuck; condition can be added if needed)
        rescue = 0

        action =  {
            "steer": steering,
            "acceleration": acceleration,
            "brake": brake,
            "drift": drift,
            "fire": fire,
            "nitro": nitro,
            "rescue": rescue
        }

        print(action)

        return action
