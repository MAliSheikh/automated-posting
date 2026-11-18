from datetime import datetime, timezone

import httpx

from app.config import settings
from app.platforms.base import BasePlatform, check_response, require
from app.schemas import URL_PATTERN


class BlueskyPlatform(BasePlatform):
    name = "Bluesky"

    async def post(self, message: str) -> str:
        require(
            BLUESKY_API_URL=settings.BLUESKY_API_URL,
            BLUESKY_HANDLE=settings.BLUESKY_HANDLE,
            BLUESKY_APP_PASSWORD=settings.BLUESKY_APP_PASSWORD,
        )

        async with httpx.AsyncClient(timeout=30) as client:
            # Step 1: log in
            session = check_response(await client.post(
                f"{settings.BLUESKY_API_URL}/com.atproto.server.createSession",
                json={
                    "identifier": settings.BLUESKY_HANDLE,
                    "password": settings.BLUESKY_APP_PASSWORD,
                },
            ))

            # Step 2: create the post record
            record = {
                "$type": "app.bsky.feed.post",
                "text": message,
                "createdAt": datetime.now(timezone.utc).isoformat(),
            }

            # Make the link clickable (Bluesky uses byte positions)
            match = URL_PATTERN.search(message)
            if match:
                start = len(message[:match.start()].encode("utf-8"))
                end = start + len(match.group().encode("utf-8"))
                record["facets"] = [{
                    "index": {"byteStart": start, "byteEnd": end},
                    "features": [{
                        "$type": "app.bsky.richtext.facet#link",
                        "uri": match.group(),
                    }],
                }]

            created = check_response(await client.post(
                f"{settings.BLUESKY_API_URL}/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {session['accessJwt']}"},
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": record,
                },
            ))

        post_id = created["uri"].split("/")[-1]
        return f"https://bsky.app/profile/{settings.BLUESKY_HANDLE}/post/{post_id}"