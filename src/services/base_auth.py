from abc import ABC, abstractmethod

class BaseAuthService(ABC):
    """
    Abstract Base Class for authentication mechanisms.
    """
    @abstractmethod
    async def generate_access_token(self):
        """generate an access token."""
        pass

    @abstractmethod
    def generate_refresh_token(self):
        """Refresh an expired access token (if supported)."""
        pass

    @abstractmethod
    def is_token_valid(self):
        """Check whether the current token is valid."""
        pass