"""
SpeedAI - Python package for SpeedAI document and text processing API

This package provides a simple interface to interact with SpeedAI's text rewriting
and AI detection reduction services.
"""

from .client import SpeedAIClient
from .exceptions import (
    SpeedAIError,
    AuthenticationError,
    ValidationError,
    ProcessingError,
    NetworkError
)
from .models import (
    TextResult,
    DocumentResult,
    ProcessingStatus,
    Language,
    Platform,
    ProcessingMode
)

__version__ = "1.0.0"
__author__ = "SpeedAI"
__all__ = [
    "SpeedAIClient",
    "SpeedAIError",
    "AuthenticationError",
    "ValidationError",
    "ProcessingError",
    "NetworkError",
    "TextResult",
    "DocumentResult",
    "ProcessingStatus",
    "Language",
    "Platform",
    "ProcessingMode"
]