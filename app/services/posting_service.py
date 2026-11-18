import asyncio

from app.platforms.bluesky import BlueskyPlatform
from app.platforms.devto import DevToPlatform
from app.platforms.facebook import FacebookPlatform
from app.platforms.instagram import InstagramPlatform
from app.platforms.threads import ThreadsPlatform
from app.schemas import PostResponse

# Platform selection is handled internally, as the test requires
PLATFORMS = [
    FacebookPlatform(),
    InstagramPlatform(),
    ThreadsPlatform(),
    DevToPlatform(),
    BlueskyPlatform(),
]


async def post_to_all(message: str) -> PostResponse:
    # Run all platforms at the same time. Each one catches its own errors.
    results = await asyncio.gather(*(p.publish(message) for p in PLATFORMS))

    return PostResponse(
        success=any(r.status == "success" for r in results),
        results=list(results),
    )