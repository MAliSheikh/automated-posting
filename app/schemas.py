import re
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator

URL_PATTERN = re.compile(r"https?://\S+")


class PostRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message must not be empty")

        if len(value) > 200:
            raise ValueError("Message must not exceed 200 characters")

        links = URL_PATTERN.findall(value)
        if len(links) != 1:
            raise ValueError("Message must contain exactly one CTA link")

        parsed = urlparse(links[0])
        if parsed.scheme not in ("http", "https") or "." not in parsed.netloc:
            raise ValueError("The link in the message is not a valid URL")

        return value


class PlatformResult(BaseModel):
    platform: str
    status: str                       # "success" or "failed"
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostResponse(BaseModel):
    success: bool                     # True if at least one platform worked
    results: list[PlatformResult]