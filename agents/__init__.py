"""
Nexus AI Adversarial Agents
Three agents with opposing objectives for legal reasoning
"""

from .paranoid_lawyer import ParanoidLawyerAgent
from .greedy_finance import GreedyFinanceAgent
from .mediator import MediatorAgent

__all__ = [
    'ParanoidLawyerAgent',
    'GreedyFinanceAgent',
    'MediatorAgent'
]
