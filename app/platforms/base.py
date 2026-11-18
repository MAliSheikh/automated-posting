from abc import ABC, abstractmethod
from datetime import datetime

import httpx

from app.schemas import PlatformResult


class PlatformError(Exception):
    """Raised when a platform fails. The message is shown in the API response."""


def check_response(response: httpx.Response) -> dict:
    """Return JSON if the call worked, otherwise raise a readable error."""
    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.status_code >= 400 or "error" in data:
        raise PlatformError(f"HTTP {response.status_code}: {response.text[:300]}")
    return data


def require(**credentials):
    """Make sure all required settings exist in .env."""
    missing = [name for name, value in credentials.items() if not value]
    if missing:
        raise PlatformError(f"Missing configuration in .env: {', '.join(missing)}")


class BasePlatform(ABC):
    name: str = "Base"

    @abstractmethod
    async def post(self, message: str) -> str:
        """Publish the message and return the public URL of the post."""

    async def publish(self, message: str) -> PlatformResult:
        """Run post() and turn success or failure into a result object."""
        try:
            url = await self.post(message)
            now = datetime.now()
            return PlatformResult(
                platform=self.name,
                status="success",
                posted_url=url,
                public_access=True,
                date=now.strftime("%Y-%m-%d"),
                time=now.strftime("%H:%M:%S"),
            )
        except Exception as error:  # one platform failing must never crash the rest
            return PlatformResult(
                platform=self.name,
                status="failed",
                public_access=False,
                error=str(error) or error.__class__.__name__,
            )