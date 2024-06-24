import logging

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
    Replaces '/' character in filenames with underscore.

    Args:
        filename (str): The original filename.

    Returns:
        str: The sanitized filename.
    """
    return filename.replace("/", "_")
