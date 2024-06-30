import json
import logging
import os
import random
from time import sleep

import requests
from bs4 import BeautifulSoup

from utils.novel_utils import (download_novel_image, get_novel_genres,
                               get_novel_image_url, get_novel_status,
                               get_novel_synopsis, get_novel_title,
                               get_number_of_volumes)
from utils.url_utils import (extract_filename_from_url, sanitize_filename,
                             url_exists)


def get_all_novels(website_base_url: str, novel_base_url: str,
                   file_name: str) -> None:
    """
    Fetches all novel URLs from the website and saves them to a JSON file.

    Args:
        website_base_url (str): The base URL of the website.
        novel_base_url (str): The base URL for novels.
        file_name (str): The name of the file where the collected URLs
        will be saved.
    """
    logging.info("(1) Getting novels...")

    index = 1
    all_novels_dict = {}

    while True:
        # Construct URL for the current index page
        if index == 1:
            # Skip index1.html since it doesn't exist
            novels_url = f"{website_base_url}index.html"
        else:
            novels_url = f"{website_base_url}index{index}.html"

        if not url_exists(novels_url):
            logging.warning(f"URL does not exist: {novels_url}")
            break

        try:
            logging.info(f"{index}: Fetching URL: {novels_url}")
            response = requests.get(novels_url)
            page_content = response.content
            soup = BeautifulSoup(page_content, "lxml")
            novel_titles = soup.find_all("h2")
            novel_links = soup.find_all("a", class_="link-a")

            # Ensure number of titles matches number of links
            if len(novel_links) != len(novel_titles):
                logging.warning(
                    f"Number of links({len(novel_links)}) and titles({len(novel_titles)}) mismatch")

            for novel_title, novel_link in zip(novel_titles, novel_links):
                novel_url = novel_link.get("href")
                filename = extract_filename_from_url(novel_url)
                novel_url = novel_base_url + filename
                sanitized_title = sanitize_filename(filename)

                all_novels_dict[sanitized_title] = novel_url
                logging.info(f"Added novel: {novel_title.text.strip()}")
        except requests.RequestException as e:
            logging.error(f"Error fetching URL {novels_url}: {e}")

        sleep(random.randrange(1, 2))
        index += 1

    # Save collected URLs to a JSON file
    try:
        with open(file_name, "w") as file:
            json.dump(all_novels_dict, file, indent=4, ensure_ascii=False)
            logging.info(f"Saved all novels to {file_name}")
    except IOError as e:
        logging.error(f"Error writing to file {file_name}: {e}")


def download_novel_html_files(file_name: str, directory: str) -> None:
    """
    Downloads the HTML files for each novel URL and saves them
    to a specified directory.

    Args:
        file_name (str): The name of the JSON file containing the novel URLs.
        directory (str): The directory where the HTML files will be saved.
    """
    logging.info(f"(2) Downloading novel HTML files to {directory}...")

    with open(file_name, "r") as file:
        all_novels = json.load(file)

    count = 0
    for novel_title, novel_url in all_novels.items():
        try:
            response = requests.get(novel_url)
            page_text = response.text

            # Do not add '.html' if it already there
            if novel_title.endswith(".html"):
                file_name = os.path.join(directory, novel_title)
            else:
                file_name = os.path.join(directory, f"{novel_title}.html")

            # Save the HTML content to a file
            try:
                with open(file_name, "w") as html_file:
                    html_file.write(page_text)
            except IOError as e:
                logging.error(f"Error writing to file {file_name}: {e}")
            count += 1
            logging.info(f"{count}: Downloaded {novel_title}")
            sleep(random.randrange(1, 2))
        except requests.RequestException as e:
            logging.error(f"Error downloading URL {novel_url}: {e}")


def get_data_from_html_files(novel_base_url: str, html_files_dir: str,
                             media_dir: str, all_novels_file: str,
                             data_file: str) -> None:
    """
    Extracts data from the downloaded HTML files and saves it to a JSON file.

    Args:
        novel_base_url (str): The base URL for novels.
        html_files_dir (str): The directory containing the
        downloaded HTML files.
        media_dir (str): The directory where media files will be saved.
        all_novels_file (str): The JSON file containing all novel URLs.
        data_file (str): The file where the extracted data will be saved.
    """
    logging.info(f"(3) Extracting data from HTML files in {html_files_dir}...")

    with open(all_novels_file, "r", encoding="utf-8") as json_file:
        all_novels = json.load(json_file)

    data_dict = []
    count = 0
    for file_name in os.listdir(html_files_dir):
        if file_name.endswith(".html"):
            file_path = os.path.join(html_files_dir, file_name)
            sanitized_title = file_name.rsplit(".", 1)[0]
            novel_url = all_novels.get(sanitized_title, "URL not found")
            if novel_url == "URL not found":
                logging.warning(f"URL wasn't found for title: {sanitized_title}")

            with open(file_path, "r", encoding="utf-8") as file:
                page_content = file.read()
                soup = BeautifulSoup(page_content, "lxml")

                # Extract novel details using helper functions
                novel_title = get_novel_title(novel_url, soup)
                novel_image_url = get_novel_image_url(novel_url, soup)
                novel_status = get_novel_status(novel_url, soup)
                novel_synopsis = get_novel_synopsis(novel_url, soup)
                novel_genres = get_novel_genres(novel_url, soup)
                novel_num_volumes = get_number_of_volumes(novel_url, soup)

                image_path = download_novel_image(
                    novel_base_url, novel_image_url, media_dir, sanitized_title)

                count += 1
                # Collect data in a dictionary
                data = {
                    "id": count,
                    "title": novel_title,
                    "status": novel_status,
                    "synopsis": novel_synopsis,
                    "genres": novel_genres,
                    "num_volumes": novel_num_volumes,
                    "image": image_path,
                    "url": novel_url
                }
                data_dict.append(data)

                logging.info(f"{count}. Processed {novel_title}")
                sleep(random.randrange(1, 2))

    # Save extracted data to a JSON file
    try:
        with open(data_file, "w") as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
            logging.info(f"Saved extracted data to {data_file}")
    except IOError as e:
        logging.error(f"Error writing to file {data_file}: {e}")
