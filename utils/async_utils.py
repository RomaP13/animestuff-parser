import logging
import os

import aiohttp
from aiohttp import ClientSession


async def fetch_html(session: ClientSession, url: str) -> str:
    """
    Fetches the HTML content of the given URL
    using the provided aiohttp ClientSession.

    Args:
        session (ClientSession): The aiohttp session to use for the request.
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL, or an empty string
        if there was an error.
    """
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"[ERROR] - Error fetching URL {url}: {e}")
        return ""


async def fetch_binary(session: ClientSession, url: str) -> bytes:
    """
    Fetches the binary content of the given URL
    using the provided aiohttp ClientSession.

    Args:
        session (ClientSession): The aiohttp session to use for the request.
        url (str): The URL to fetch the binary content from.

    Returns:
        bytes: The binary content of the URL, or an empty bytes object
        if there was an error.
    """
    try:
        async with session.get(url) as response:
            return await response.read()
    except aiohttp.ClientError as e:
        logging.error(f"[ERROR] - Error fetching URL {url}: {e}")
        return b""


async def url_exists(session: ClientSession, url: str) -> bool:
    """
    Checks if the given URL exists by making a HEAD request
    using the provided aiohttp ClientSession.

    Args:
        session (ClientSession): The aiohttp session to use for the request.
        url (str): The URL to check.

    Returns:
        bool: True if the URL exists, False otherwise.
    """
    try:
        async with session.head(url, allow_redirects=True) as response:
            return response.status == 200
    except aiohttp.ClientError as e:
        logging.error(f"[ERROR] - Error checking URL {url}: {e}")
        return False


async def download_novel_image(session: ClientSession, novel_base_url: str,
                               novel_image_url: str, media_dir: str,
                               sanitized_title: str) -> str:
    """
    Downloads a novel image from the given URL and
    saves it to the specified media directory.

    Args:
        session (ClientSession): The aiohttp session to use for the request.
        novel_base_url (str): The base URL of the novel website.
        novel_image_url (str): The URL of the novel image.
        media_dir (str): The directory to save the downloaded image.
        sanitized_title (str): The sanitized title of the novel
        used as the image file name.

    Returns:
        str: The path to the saved image, or "Not found"
        if the image could not be downloaded.
    """
    # Check if image url is on another website
    if not novel_image_url.startswith("https"):
        novel_image_url = novel_base_url + novel_image_url

    if not await url_exists(session, novel_image_url):
        logging.warning(
            f"[WARNING] - Image URL does not exist: {novel_image_url}")
        return "Not found"

    # Download the image
    content = await fetch_binary(session, novel_image_url)
    if not content:
        return "Not found"

    # Save the image to the media directory
    image_path = os.path.join(media_dir, f"{sanitized_title}.png")
    with open(image_path, "wb") as image:
        image.write(content)

    return image_path
