import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.EulerAgent import EulerAgent  # Import du nouvel agent optimisé

if __name__ == "__main__":
    agent = EulerAgent(track=None, render_mode="human")  # Utilisation par défaut du path_lookahead = 3

    # Exemple d'ajustement du path_lookahead si nécessaire
    # agent = EulerAgent(track=None, render_mode="human", path_lookahead=4)

    # Exécution de l'agent en consommant le générateur
    for obs in agent.run():
        pass
