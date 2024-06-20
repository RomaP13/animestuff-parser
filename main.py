import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


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


def get_novels_url_list(base_url: str, file_name: str) -> None:
    """
    Scrapes novel URLs from a website and saves them to a file.
    Args:
        base_url (str): The base URL of the website.
        file_name (str): The name of the output file.
    """
    index = 1
    novels_url_list = []

    # while True:
    while index < 5:
        if index == 1:
            # Skip index1.html since it doesn't exist
            novels_url = f"{base_url}index.html"
        else:
            novels_url = f"{base_url}index{index}.html"

        if not url_exists(novels_url):
            logging.warning(f"URL does not exist: {novels_url}")
            break

        try:
            response = requests.get(novels_url)
            page_content = response.content
            soup = BeautifulSoup(page_content, "lxml")
            novel_links = soup.find_all("a", class_="link-a")

            for novel_link in novel_links:
                novel_page_url = novel_link.get("href")
                novels_url_list.append(novel_page_url)
        except requests.RequestException as e:
            logging.error(f"Error fetching URL {novels_url}: {e}")

        index += 1

    try:
        with open(file_name, "a") as file:
            for line in novels_url_list:
                file.write(f"{line}\n")
    except IOError as e:
        logging.error(f"Error writing to file {file_name}: {e}")


def main() -> None:
    URL = "https://animestuff.me/"
    FILE_NAME = "novels_url_list.txt"

    get_novels_url_list(URL, FILE_NAME)


if __name__ == "__main__":
    main()
