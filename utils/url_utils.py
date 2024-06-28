import logging
import re

import requests


def url_exists(url: str) -> bool:
    """
    Check if a given URL exists by making a HEAD request.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL exists (status code 200), False otherwise.
    """
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Error checking URL {url}: {e}")
        return False


def extract_filename_from_url(url: str) -> str:
    """
    Extracts the filename from a URL.

    Args:
        url (str): The URL to extract the filename from.

    Returns:
        str: The extracted filename.
    """
    filename = url.split("/")[-1]
    if filename.startswith("html"):
        return filename[len("html"):]

    return filename


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename by removing or replacing characters that are not
    allowed or could cause issues in file paths.

    Args:
        filename (str): The original filename.

    Returns:
        str: The sanitized filename.
    """
    sanitized_filename = re.sub(r"[<>:'/\\|?*\'']", "", filename)
    sanitized_filename = sanitized_filename.replace(
        " ", "_").replace("%20", "_")
    if sanitized_filename.endswith(".html"):
        sanitized_filename = sanitized_filename[:-5]

    return sanitized_filename
