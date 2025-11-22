"""
Nexus AI Council Agents
Three specialized agents for business compliance deliberation
"""

from .legal_scholar import LegalScholarAgent
from .tax_comptroller import TaxComptrollerAgent
from .growth_hacker import GrowthHackerAgent

__all__ = [
    'LegalScholarAgent',
    'TaxComptrollerAgent',
    'GrowthHackerAgent'
]
