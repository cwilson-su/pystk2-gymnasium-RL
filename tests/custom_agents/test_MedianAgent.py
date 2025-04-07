"""
Ce script lance une simulation solo avec MedianAgent dans une course sur la piste "zengarden".
L'agent est contrôlé par MedianAgent et s'exécute dans l'environnement STKRaceEnv.
"""

import sys
import os
# Ajoute le dossier "src" au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

from customAgents.MedianAgent import MedianAgent
from pystk2_gymnasium.envs import STKRaceEnv, AgentSpec
from pystk2_gymnasium.envs import get_action  # si nécessaire pour convertir des actions

# Spécification de l'agent (course solo: on utilise rank_start = 0)
agent_spec = AgentSpec(name="Median", rank_start=0, use_ai=False)

# Création de l'environnement solo avec STKRaceEnv
env = STKRaceEnv(agent=agent_spec, track="black_forest", render_mode="human")

# Instanciation de MedianAgent avec le paramètre path_lookahead (exemple : 3)
median_agent = MedianAgent(env, path_lookahead=3)

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        # MedianAgent calcule l'action à partir de l'observation
        action = median_agent.calculate_action(obs)
        obs, reward, done, truncated, info = env.step(action)
        print("Récompense :", reward)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
