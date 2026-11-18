import asyncio

import httpx

from app.config import settings
from app.platforms.base import BasePlatform, PlatformError, check_response, require


class InstagramPlatform(BasePlatform):
    name = "Instagram"

    async def post(self, message: str) -> str:
        # Instagram does NOT allow text-only posts, so an image is required.
        require(
            FB_GRAPH_API_URL=settings.FB_GRAPH_API_URL,
            IG_USER_ID=settings.IG_USER_ID,
            FB_PAGE_ACCESS_TOKEN=settings.FB_PAGE_ACCESS_TOKEN,
            IG_IMAGE_URL=settings.IG_IMAGE_URL,
        )

        token = settings.FB_PAGE_ACCESS_TOKEN

        async with httpx.AsyncClient(timeout=60) as client:
            # Step 1: create a media container
            container = check_response(await client.post(
                f"{settings.FB_GRAPH_API_URL}/{settings.IG_USER_ID}/media",
                data={
                    "image_url": settings.IG_IMAGE_URL,
                    "caption": message,
                    "access_token": token,
                },
            ))

            await asyncio.sleep(5)

            # Step 2: publish after Instagram finishes processing the container
            for attempt in range(3):
                response = await client.post(
                    f"{settings.FB_GRAPH_API_URL}/{settings.IG_USER_ID}/media_publish",
                    data={"creation_id": container["id"], "access_token": token},
                )
                try:
                    published = check_response(response)
                    break
                except PlatformError as error:
                    try:
                        body = response.json()
                    except ValueError:
                        body = {}
                    api_error = body.get("error") if isinstance(body, dict) else None
                    if (
                        not isinstance(api_error, dict)
                        or api_error.get("error_subcode") != 2207027
                        or attempt == 2
                    ):
                        raise error
                    await asyncio.sleep(5)

            # Step 3: get the public link of the new post
            info = check_response(await client.get(
                f"{settings.FB_GRAPH_API_URL}/{published['id']}",
                params={"fields": "permalink", "access_token": token},
            ))

        return info["permalink"]