# tests/__init__.py

# Import key test modules
from .custom_agents import FollowTrackNodesAgent, StayInMiddleAgent
from .given_agents import multi_AI_customActionS_CSV, multi_AI_customActionS_GRAPH
from .unit_tests import test_consistency, test_envs

# Define __all__ to specify available modules
__all__ = [
    "custom_agents",
    "given_agents",
    "unit_tests",
]

