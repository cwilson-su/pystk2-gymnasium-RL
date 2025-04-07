#!/usr/bin/env python3
"""
Ce script lance une simulation solo avec EulerAgent dans une course sur la piste "zengarden".
L'agent est contrôlé par EulerAgent et s'exécute dans l'environnement STKRaceEnv.
"""

import sys
import os
# Ajoute le dossier "src" au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

from customAgents.EulerAgent import EulerAgent
from pystk2_gymnasium.envs import STKRaceEnv, AgentSpec
from pystk2_gymnasium.envs import get_action  # si nécessaire pour convertir des actions

# Spécification de l'agent (course solo: on utilise rank_start = 0)
agent_spec = AgentSpec(name="Euler", rank_start=0, use_ai=False)

# Création de l'environnement solo avec STKRaceEnv
env = STKRaceEnv(agent=agent_spec, track="black_forest", render_mode="human")

# Instanciation d'EulerAgent avec le paramètre path_lookahead (exemple : 3)
euler_agent = EulerAgent(env, path_lookahead=3)

def main():
    obs, _ = env.reset()
    done = False
    while not done:
        # EulerAgent calcule l'action à partir de l'observation
        action = euler_agent.calculate_action(obs)
        obs, reward, done, truncated, info = env.step(action)
        if done or truncated:
            break
    env.close()

if __name__ == "__main__":
    main()
