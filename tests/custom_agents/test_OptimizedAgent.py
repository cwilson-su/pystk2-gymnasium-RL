import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
from customAgents.OptimizedMedianAgent import OptimizedMedianAgent

if __name__ == "__main__":
    agent = OptimizedMedianAgent(track= 'black_forest', render_mode="human", plot=True)  
    
    
    for obs in agent.run():
        pass
