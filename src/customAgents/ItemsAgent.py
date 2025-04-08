import numpy as np

# Mapping of item type codes to names for debug outputs
ITEM_TYPE_NAMES = {
    0: "BONUS_BOX",
    1: "BANANA",
    2: "NITRO_BIG",
    3: "NITRO_SMALL",
    4: "BUBBLEGUM",
    6: "EASTER_EGG"
}

class ItemsAgent:
    """
    An agent similar to EulerAgent but augmented with the ability to 'see' items,
    and to use any powerup it possesses immediately.
    
    It uses both base path-following behavior and enriched observations (such as
    target item position, distance, angle, and type) to decide whether to approach
    or avoid an item. In addition, if the observation indicates that a powerup is available,
    the agent will use it by setting the fire flag to True.
    """
    def __init__(self, env, path_lookahead=3):
        # The agent receives the environment so that only one simulation runs.
        self.env = env
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None

    def reset(self):
        """Resets the environment and initializes the agent."""
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def calculate_action(self):
        """
        Computes the action based on a combination of base path-following (as in EulerAgent),
        augmented item observations (target_item_position, target_item_distance, target_item_angle,
        and target_item_type), and the current powerup held.
        
        If a target item is close, the agent will either approach it (if it's a 'good' item)
        or avoid it (if it's a 'bad' item). Additionally, if the agent has a powerup (i.e. powerup != 0),
        the agent will use it by setting the 'fire' flag to True.
        """
        obs = self.obs
        
        # --- Base Path-Following ---
        # Use the centerline's target node from the observation
        path_ends = obs["paths_end"][:self.path_lookahead]
        path_end = path_ends[-1]
        kart_front = obs["front"]
        direction_to_target = path_end - kart_front
        base_steering = 0.4 * direction_to_target[0]
        
        # Compute a base acceleration (you can refine this further)
        curvature = 0.1  # Placeholder value; you can compute actual curvature if desired
        acceleration = max(0.5, 1 - abs(curvature))
        
        steering = base_steering

        # --- Augmented Item Perception ---
        # The observation wrapper should add the following keys:
        #   target_item_position, target_item_distance, target_item_angle, target_item_type
        target_distance = obs.get("target_item_distance", np.array([np.inf]))[0]
        target_angle = obs.get("target_item_angle", np.array([0]))[0]
        target_type = obs.get("target_item_type", 0)
        # For debug: get the human-readable item name.
        item_name = ITEM_TYPE_NAMES.get(target_type, "UNKNOWN")
        print(f"Item target: {item_name}, distance {target_distance:.2f}, angle {target_angle:.2f}")
        
        # Define which item types are good and which are bad.
        # Example: BONUS_BOX, NITRO_BIG, NITRO_SMALL, EASTER_EGG are good; BANANA and BUBBLEGUM are bad.
        good_types = [0, 2, 3, 6]
        bad_types = [1, 4]
        
        if target_distance < 10:
            target_item_pos = obs.get("target_item_position", np.array([0, 0, 0]))
            if target_type in good_types:
                # Steer toward the item by adding a small steering offset based on lateral (X) component.
                steering += 0.1 * target_item_pos[0]
                print("Approaching good item.")
            elif target_type in bad_types:
                # Steer away from the item by subtracting a small steering offset.
                steering -= 0.1 * target_item_pos[0]
                print("Avoiding bad item.")
        #else:
        #    print("No target item in close range; following base path.")

        # --- Powerup Usage ---
        # Check if the observation indicates that the kart has a powerup.
        # Typically, a powerup value of 0 means no powerup.
        if obs.get("powerup", 0) != 0:
            fire = True
            print(">>>>>>> Using powerup.")
        else:
            fire = False

        # Final adjustments and clipping.
        steering = np.clip(steering, -1, 1)
        
        # Record current position for visualization.
        agent_abs_pos = np.array(self.env.unwrapped.world.karts[0].location)
        self.agent_positions.append(agent_abs_pos)
        
        action = {
            "acceleration": np.clip(acceleration, 0.5, 1),
            "steer": steering,
            "brake": False,
            "drift": False,
            "nitro": False,
            "rescue": True,
            "fire": fire
        }
        return action

    def step(self):
        action = self.calculate_action()
        self.obs, reward, done, truncated, info = self.env.step(action)
        return done

    def run(self, steps=10000):
        self.reset()
        for step in range(steps):
            done = self.step()
            yield self.obs
            if done:
                break
        self.env.close()
