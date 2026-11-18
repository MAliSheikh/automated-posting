from datetime import datetime

import httpx

from app.config import settings
from app.platforms.base import BasePlatform, check_response, require


class DevToPlatform(BasePlatform):
    name = "Dev.to"

    async def post(self, message: str) -> str:
        require(
            DEVTO_API_URL=settings.DEVTO_API_URL,
            DEVTO_API_KEY=settings.DEVTO_API_KEY,
        )

        # Dev.to needs a title, so we make one with the time to keep it unique
        title = f"Update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                settings.DEVTO_API_URL,
                headers={"api-key": settings.DEVTO_API_KEY},
                json={
                    "article": {
                        "title": title,
                        "body_markdown": message,
                        "published": True,
                    }
                },
            )
            data = check_response(response)

        return data["url"]