import httpx

from app.config import settings
from app.platforms.base import BasePlatform, check_response, require


class FacebookPlatform(BasePlatform):
    name = "Facebook"

    async def post(self, message: str) -> str:
        require(
            FB_GRAPH_API_URL=settings.FB_GRAPH_API_URL,
            FB_PAGE_ID=settings.FB_PAGE_ID,
            FB_PAGE_ACCESS_TOKEN=settings.FB_PAGE_ACCESS_TOKEN,
        )

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{settings.FB_GRAPH_API_URL}/{settings.FB_PAGE_ID}/feed",
                data={
                    "message": message,
                    "access_token": settings.FB_PAGE_ACCESS_TOKEN,
                },
            )
            data = check_response(response)

        post_id = data["id"]  # looks like "PAGEID_POSTID"
        return f"https://www.facebook.com/{post_id}"