import numpy as np

"""
A further decorator that adds item-based decision making (including powerup usage) on top of an existing agent(typically an EulerAgent).
"""

# Mapping of item type codes to names for debugging.
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
    An agent that wraps another agent (e.g., EulerAgent or MedianAgent) and
    augments its decisions with item information. It uses enriched observations
    (such as target_item_position, target_item_distance, target_item_angle,
    and target_item_type) to decide whether to approach a good item or avoid a bad one.
    It also uses any powerup in its possession.
    """
    def __init__(self, wrapped_agent):
        self.agent = wrapped_agent
        self.env = wrapped_agent.env
        self.path_lookahead = wrapped_agent.path_lookahead
        self.agent_positions = wrapped_agent.agent_positions
        self.obs = None

    def reset(self):
        self.agent.reset()
        self.obs = self.agent.obs

    def calculate_action(self, obs):
        # Get base action from the wrapped agent.
        base_action = self.agent.calculate_action(obs)
        
        # Extract enriched item information.
        target_distance = obs.get("target_item_distance", np.array([np.inf]))[0]
        target_angle = obs.get("target_item_angle", np.array([0]))[0]
        target_type = obs.get("target_item_type", 0)
        item_name = ITEM_TYPE_NAMES.get(target_type, "UNKNOWN")
        print(f"Item target: {item_name}, distance {target_distance:.2f}, angle {target_angle:.2f}")
        
        # Define which item types are considered good and which are bad.
        good_types = [0, 2, 3, 6]  # e.g., BONUS_BOX, NITRO_BIG, NITRO_SMALL, EASTER_EGG
        bad_types = [1, 4]         # e.g., BANANA, BUBBLEGUM

        if target_distance < 10:
            target_item_pos = obs.get("target_item_position", np.array([0, 0, 0]))
            if target_type in good_types:
                base_action["steer"] += 0.1 * target_item_pos[0]
                print("Approaching good item.")
            elif target_type in bad_types:
                base_action["steer"] -= 0.1 * target_item_pos[0]
                print("Avoiding bad item.")
        
        # Use powerup if available (nonzero powerup indicates possession).
        if obs.get("powerup", 0) != 0:
            base_action["fire"] = True
            print("Using powerup.")
        else:
            base_action["fire"] = False

        base_action["steer"] = np.clip(base_action["steer"], -1, 1)
        return base_action

    def step(self):
        action = self.calculate_action(self.obs)
        self.obs, reward, done, truncated, info = self.env.step(action)
        self.agent_positions.append(np.array(self.env.unwrapped.world.karts[0].location))
        return done

    def run(self, steps=10000):
        self.reset()
        for _ in range(steps):
            done = self.step()
            yield self.obs
            if done:
                break
        self.env.close()
