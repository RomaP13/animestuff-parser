import asyncio
import json
import logging
import random
from typing import Any, Dict, List

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from utils.async_utils import download_novel_image, fetch_html, url_exists
from utils.novel_utils import (get_novel_genres, get_novel_image_url,
                               get_novel_status, get_novel_synopsis,
                               get_novel_title, get_number_of_volumes)
from utils.url_utils import extract_filename_from_url, sanitize_filename

data_dict: List[Dict[str, Any]] = []


async def gather_novels_data(website_base_url: str, novel_base_url: str,
                             media_dir: str, data_file: str) -> None:
    """
    Gathers data for all novels from the given website and
    saves it to a JSON file.

    Args:
        website_base_url (str): The base URL of the website.
        novel_base_url (str): The base URL for novels.
        media_dir (str): The directory to save downloaded novel images.
        data_file (str): The file where the extracted data will be saved.

    """
    logging.info("[INFO] - Getting novels...")

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    tasks = []
    index = 1
    id = 1
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            # Construct URL for the current index page
            if index == 1:
                # Skip index1.html since it doesn't exist
                novels_url = f"{website_base_url}index.html"
            else:
                novels_url = f"{website_base_url}index{index}.html"

            if not await url_exists(session, novels_url):
                logging.warning(
                    f"[WARNING] - URL does not exist: {novels_url}")
                break

            logging.info(f"[INFO] - ({index}): Fetching URL: {novels_url}")
            page_content = await fetch_html(session, novels_url)
            if not page_content:
                continue
            soup = BeautifulSoup(page_content, "lxml")
            novel_titles = soup.find_all("h2")
            novel_links = soup.find_all("a", class_="link-a")

            # Ensure number of titles matches number of links
            if len(novel_links) != len(novel_titles):
                logging.warning(f"[WARNING] - Number of links({len(novel_links)}) and titles({len(novel_titles)}) mismatch")

            for novel_title, novel_link in zip(novel_titles, novel_links):
                novel_url = novel_link.get("href")
                filename = extract_filename_from_url(novel_url)
                novel_url = novel_base_url + filename
                sanitized_title = sanitize_filename(filename)

                task = asyncio.create_task(
                    get_novel_data(
                        session,
                        novel_base_url,
                        novel_url,
                        media_dir,
                        sanitized_title,
                        id
                    )
                )
                tasks.append(task)
                id += 1

            await asyncio.sleep(random.uniform(1, 2))
            index += 1

        await asyncio.gather(*tasks)

    # Save extracted data to a JSON file
    try:
        with open(data_file, "w") as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
            logging.info(f"[INFO] - Saved extracted data to {data_file}")
    except IOError as e:
        logging.error(f"[ERROR] - Error writing to file {data_file}: {e}")


async def get_novel_data(session: ClientSession, novel_base_url: str,
                         novel_url: str, media_dir: str,
                         sanitized_title: str, id: int) -> None:
    """
    Extracts data for a single novel and appends it
    to the global data dictionary.

    Args:
        session (ClientSession): The aiohttp session to use for the request.
        novel_base_url (str): The base URL for novels.
        novel_url (str): The URL of the novel page.
        media_dir (str): The directory where media files will be saved.
        sanitized_title (str): The sanitized title of the novel
        used as the image file name.
        id (int): The ID of the novel.
    """
    logging.info(f"[INFO] - Extracting novel data from {novel_url}...")

    if not await url_exists(session, novel_url):
        logging.warning(f"[WARNING] - URL does not exist: {novel_url}.")
        return

    page_content = await fetch_html(session, novel_url)
    if not page_content:
        return

    soup = BeautifulSoup(page_content, "lxml")

    # Extract novel details using helper functions
    novel_title = get_novel_title(novel_url, soup)
    novel_image_url = get_novel_image_url(novel_url, soup)
    novel_status = get_novel_status(novel_url, soup)
    novel_synopsis = get_novel_synopsis(novel_url, soup)
    novel_genres = get_novel_genres(novel_url, soup)
    novel_num_volumes = get_number_of_volumes(novel_url, soup)

    image_path = await download_novel_image(
        session,
        novel_base_url,
        novel_image_url,
        media_dir, sanitized_title
    )

    # Collect data in a dictionary
    data = {
        "id": id,
        "title": novel_title,
        "status": novel_status,
        "synopsis": novel_synopsis,
        "genres": novel_genres,
        "num_volumes": novel_num_volumes,
        "image": image_path,
        "url": novel_url
    }

    logging.info(f"[INFO] - {id}. Processed {novel_title}")
    data_dict.append(data)
