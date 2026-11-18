import asyncio

import httpx

from app.config import settings
from app.platforms.base import BasePlatform, PlatformError, check_response, require


class ThreadsPlatform(BasePlatform):
    name = "Threads"

    async def post(self, message: str) -> str:
        require(
            THREADS_GRAPH_API_URL=settings.THREADS_GRAPH_API_URL,
            THREADS_ACCESS_TOKEN=settings.THREADS_ACCESS_TOKEN,
        )

        token = settings.THREADS_ACCESS_TOKEN

        async with httpx.AsyncClient(timeout=60) as client:
            # Step 1: create the post container
            container = check_response(await client.post(
                f"{settings.THREADS_GRAPH_API_URL}/me/threads",
                data={"media_type": "TEXT", "text": message, "access_token": token},
            ))

            # Wait, because Threads needs a few seconds
            await asyncio.sleep(5)

            # Step 2: publish it
            published = check_response(await client.post(
                f"{settings.THREADS_GRAPH_API_URL}/me/threads_publish",
                data={"creation_id": container["id"], "access_token": token},
            ))

            # Step 3: get the link (try up to 3 times)
            info = None
            last_error = None
            for _ in range(3):
                await asyncio.sleep(2)
                try:
                    info = check_response(await client.get(
                        f"{settings.THREADS_GRAPH_API_URL}/{published['id']}",
                        params={"fields": "permalink", "access_token": token},
                    ))
                    break
                except (httpx.HTTPError, PlatformError) as error:
                    last_error = error

        if info is None:
            raise PlatformError(
                f"Posted, but could not get the link: {last_error}"
            ) from last_error

        return info["permalink"]