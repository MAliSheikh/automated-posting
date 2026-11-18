import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file


class Settings:
    # Facebook / Instagram
    FB_GRAPH_API_URL = os.getenv("FB_GRAPH_API_URL")
    FB_PAGE_ID = os.getenv("FB_PAGE_ID")
    FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
    IG_USER_ID = os.getenv("IG_USER_ID")
    IG_IMAGE_URL = os.getenv("IG_IMAGE_URL")

    # Threads
    THREADS_GRAPH_API_URL = os.getenv("THREADS_GRAPH_API_URL")
    THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")

    # Dev.to
    DEVTO_API_URL = os.getenv("DEVTO_API_URL")
    DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")

    # Bluesky
    BLUESKY_API_URL = os.getenv("BLUESKY_API_URL")
    BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
    BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")


settings = Settings()