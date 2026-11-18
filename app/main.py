from fastapi import FastAPI

from app.schemas import PostRequest, PostResponse
from app.services.posting_service import post_to_all

app = FastAPI(title="Automated Multi-Platform Posting System")


@app.post("/posting", response_model=PostResponse)
async def create_posting(request: PostRequest):
    """Validates the message and posts it to all platforms."""
    return await post_to_all(request.message)