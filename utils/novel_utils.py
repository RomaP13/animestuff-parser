import logging
import os
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from utils.url_utils import url_exists


def find_header_by_partial_match(soup: BeautifulSoup,
                                 keyword: str) -> Optional[Tag]:
    """
    Finds the first header (h1, h2, h3, etc.) containing
    the specified keyword (case-insensitive).

    Args:
        soup (BeautifulSoup): The parsed HTML content.
        keyword (str): The keyword to search for in header text.

    Returns:
        Optional[Tag]: The header tag if found, or None if not found.
    """
    # Find all header tags (h1, h2, h3, etc.)
    headers = soup.find_all(re.compile(r'^h\d$'))
    for header in headers:
        if keyword.lower() in header.text.lower():
            return header

    return None


def get_novel_title(novel_url: str, soup: BeautifulSoup) -> str:
    """
    Retrieves the title of a novel from a BeautifulSoup object.

    Args:
        novel_url (str): The URL of the novel.
        soup (BeautifulSoup): A BeautifulSoup object representing
        the parsed HTML content.

    Returns:
        str: The novel title or "Not found" if the title cannot be retrieved.
    """
    title = soup.find("title")

    # If the page does not have a title, then try to find it in the headers
    if not title or not title.text.strip():
        title = find_header_by_partial_match(soup, "EPUB")

    if title:
        novel_title = title.text.strip()
        # Remove '(EPUB)' from the title
        novel_title = novel_title.replace("(EPUB)", "")

        if novel_title:
            return novel_title
        else:
            logging.warning(f"Novel title wasn't found. URL: {novel_url}")
    else:
        logging.warning(f"Novel title header wasn't found. URL: {novel_url}")

    return "Not found"


def get_novel_image_url(novel_url: str, soup: BeautifulSoup) -> str:
    """
    Extracts the URL of the novel's cover image from a BeautifulSoup object.

    Args:
        novel_url (str): The URL of the novel.
        soup (BeautifulSoup): A BeautifulSoup object representing
        the parsed HTML content.

    Returns:
        str: The URL of the novel's cover image or "Not found".
    """
    div_tag = soup.find(class_="ani")
    if not div_tag:
        logging.warning(f"Div tag not found for URL: {novel_url}")
        return "Not found"

    image_tag = div_tag.find("img")
    if not isinstance(image_tag, Tag):
        logging.warning(f"Image tag not found for URL: {novel_url}")
        return "Not found"

    image_url = image_tag.get("src", "")
    if not image_url:
        logging.warning(f"Image URL not found for URL: {novel_url}")
        return "Not found"

    return image_url


def get_novel_status(novel_url: str, soup: BeautifulSoup) -> str:
    """
    Retrieves the status of a novel from a BeautifulSoup object.

    Args:
        novel_url (str): The URL of the novel.
        soup (BeautifulSoup): A BeautifulSoup object representing
        the parsed HTML content.

    Returns:
        str: The novel status or "Not found".
    """
    status_header = find_header_by_partial_match(soup, "status")

    if status_header:
        novel_status = status_header.find_next_sibling("p")
        if novel_status:
            return novel_status.text.strip()
        else:
            logging.warning(f"Novel status wasn't found. URL: {novel_url}")
    else:
        logging.warning(f"Novel status header wasn't found. URL: {novel_url}")

    return "Not found"


def get_novel_synopsis(novel_url: str, soup: BeautifulSoup) -> str:
    """
    Retrieves the synopsis of a novel from a BeautifulSoup object.

    Args:
        novel_url (str): The URL of the novel.
        soup (BeautifulSoup): A BeautifulSoup object representing
        the parsed HTML content.

    Returns:
        str: The novel synopsis or "Not found".
    """
    synopsis_header = find_header_by_partial_match(soup, "synopsis")

    if synopsis_header:
        novel_synopsis = synopsis_header.find_next_sibling("p")
        if novel_synopsis:
            return novel_synopsis.text.strip()
        else:
            logging.warning(f"Novel synopsis wasn't found. URL: {novel_url}")
    else:
        logging.warning(
            f"Novel synopsis header wasn't found. URL: {novel_url}")

    return "Not found"


def get_novel_genres(novel_url: str, soup: BeautifulSoup) -> str:
    """
    Retrieves the genres of a novel from a BeautifulSoup object.

    Args:
        novel_url (str): The URL of the novel.
        soup (BeautifulSoup): A BeautifulSoup object representing
        the parsed HTML content.

    Returns:
        str: The novel genres or "Not found".
    """
    genre_header = find_header_by_partial_match(soup, "genre")

    if genre_header:
        novel_genres = genre_header.find_next_sibling("p")
        if novel_genres:
            return novel_genres.text.strip()
        else:
            logging.warning(f"Novel genres weren't found. URL: {novel_url}")
    else:
        logging.warning(f"Novel genre header wasn't found. URL: {novel_url}")

    return "Not found"


def get_number_of_volumes(novel_url: str, soup: BeautifulSoup) -> int:
    """
    Retrieves the number of volumes of a novel from a BeautifulSoup object.

    Args:
        novel_url (str): The URL of the novel.
        soup (BeautifulSoup): A BeautifulSoup object representing
        the parsed HTML content.

    Returns:
        int: The number of volumes or 0 if the volumes cannot be retrieved.
    """
    volume_header = find_header_by_partial_match(soup, "download")

    if volume_header:
        # Count the number of "a" tags after the volume header,
        # excluding the last one
        novel_num_volumes = len(volume_header.find_all_next("a")) - 1
        if novel_num_volumes > 0:
            return novel_num_volumes
        else:
            logging.warning(f"Novel volumes weren't found. URL: {novel_url}")
    else:
        logging.warning(f"Novel volumes weren't found. URL: {novel_url}")

    return 0


def download_novel_image(novel_base_url: str, novel_image_url: str,
                         media_dir: str, sanitized_title: str) -> str:
    """
    Downloads the novel image and saves it to the media directory.

    Args:
        novel_base_url (str): The base URL of the novel website.
        novel_image_url (str): The URL or partial URL of the novel image.
        media_dir (str): The directory where media files will be saved.
        sanitized_title (str): The sanitized title of the novel used for naming
        the saved image file.

    Returns:
        str: The file path where the image is saved, or "Not found"
        if the image could not be downloaded.
    """
    # Check if image url is on another website
    if not novel_image_url.startswith("https"):
        novel_image_url = novel_base_url + novel_image_url

    # Download image
    if not url_exists(novel_image_url):
        logging.warning(f"Image URL does not exist: {novel_image_url}")
        image_path = "Not found"
    else:
        try:
            response = requests.get(novel_image_url)
        except requests.RequestException as e:
            logging.error(f"Error fetching URL {novel_image_url}: {e}")
            image_path = "Not found"
        else:
            # Save the image
            image_path = os.path.join(media_dir, f"{sanitized_title}.png")
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, "wb") as image:
                image.write(response.content)

    return image_path
