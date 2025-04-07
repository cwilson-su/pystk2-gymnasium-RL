#!/usr/bin/env python3
"""
Ce script lance une simulation avec deux agents (MedianAgent et EulerAgent) dans une même course.
Il utilise l'environnement multi-agent (STKRaceMultiEnv) de SuperTuxKart.
"""

import sys
import os

# Ajout du dossier "src" au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))

# Importation des agents personnalisés et de l'environnement
from customAgents.MedianAgent import MedianAgent
from customAgents.EulerAgent import EulerAgent
from pystk2_gymnasium.envs import STKRaceMultiEnv, AgentSpec

# Patch pour rendre AgentSpec hashable (nécessaire pour l'utilisation de set() dans STKRaceMultiEnv)
def agent_spec_hash(self):
    return hash((self.rank_start, self.use_ai, self.name, self.camera_mode))

AgentSpec.__hash__ = agent_spec_hash

# Création des spécifications pour chaque agent.
agents_specs = [
    AgentSpec(name="Median", rank_start=1, use_ai=False),  # MedianAgent sur le kart d'indice 1
    AgentSpec(name="Euler",  rank_start=2, use_ai=False)    # EulerAgent sur le kart d'indice 2
]

# Création de l'environnement multi-agent avec la piste "zengarden" et le mode "human"
env = STKRaceMultiEnv(agents=agents_specs, track=None, render_mode="human")

# Instanciation des agents personnalisés avec l'environnement.
# Le paramètre path_lookahead permet de définir le nombre de segments de la piste considérés.
median_agent = MedianAgent(env, path_lookahead=3)
euler_agent  = EulerAgent(env, path_lookahead=3)

def main():
    # Démarrage de la simulation.
    obs, _ = env.reset()
    done = False
    while not done:
        actions = {}
        # L'environnement multi-agent retourne un dictionnaire d'observations avec des clés "0", "1", ...
        # Ici, on suppose que "0" correspond à MedianAgent et "1" à EulerAgent.
        actions["0"] = median_agent.calculate_action(obs["0"])
        actions["1"] = euler_agent.calculate_action(obs["1"])

        obs, reward, done, truncated, info = env.step(actions)
        if done or truncated:
            break

    env.close()

if __name__ == "__main__":
    main()
