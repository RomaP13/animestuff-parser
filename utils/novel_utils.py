import logging
import re
from typing import Optional

from bs4 import BeautifulSoup, Tag


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
    print(headers)
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

    if not title or not title.text.strip():
        title = find_header_by_partial_match(soup, "EPUB")

    if title:
        novel_title = title.text.strip()
        if novel_title:
            return novel_title
        else:
            logging.warning(f"Novel title wasn't found. URL: {novel_url}")
    else:
        logging.warning(f"Novel title header wasn't found. URL: {novel_url}")

    return "Not found"


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
