"""
Exception classes for SpeedAI SDK.
"""


class SpeedAIError(Exception):
    """Base exception for all SpeedAI SDK errors."""
    pass


class AuthenticationError(SpeedAIError):
    """Raised when authentication fails or credentials are invalid."""
    pass


class ValidationError(SpeedAIError):
    """Raised when input validation fails."""
    pass


class ProcessingError(SpeedAIError):
    """Raised when API processing fails."""
    pass


class NetworkError(SpeedAIError):
    """Raised when network communication fails."""
    pass