# config/__init__.py
"""
Configuration module for TexLM.
Exports client and prompts for easy access.
"""

from .config import get_client
from . import prompts

__all__ = ['get_client', 'prompts']

