import os
import asyncio
from modules.logging_config import setup_logging
from modules.async_novel_parser import gather_novels_data


def main() -> None:
    WEBSITE_BASE_URL = "https://animestuff.me/"
    NOVEL_BASE_URL = "https://animestuff.me/docs/assets/html/"
    MEDIA_DIR = "static/media"
    DATA_DIR = "data"
    DATA_FILE = os.path.join(DATA_DIR, "novels_data.json")

    # Create necessary directories
    os.makedirs(MEDIA_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # Run the asynchronous task
    asyncio.run(gather_novels_data(
        WEBSITE_BASE_URL, NOVEL_BASE_URL, MEDIA_DIR, DATA_FILE
    ))


if __name__ == "__main__":
    setup_logging()
    main()
