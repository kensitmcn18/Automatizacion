"""
mews package - MEWS API integration
"""

from .client import MewsClient
from . import endpoints

__all__ = ['MewsClient', 'endpoints']
