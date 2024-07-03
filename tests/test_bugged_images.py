import unittest

import aiohttp
import requests
from bs4 import BeautifulSoup

from utils.async_utils import \
    download_novel_image as async_download_novel_image
from utils.novel_utils import download_novel_image, get_novel_image_url


class TestNovelImageExtraction(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class variables and read URLs from the input file."""
        filename = "tests/data/urls_with_bugged_images.txt"
        cls.urls = []
        cls.novel_base_url = "https://animestuff.me/docs/assets/html/"
        cls.media_dir = "static/media/"

        try:
            with open(filename, "r") as file:
                for line in file:
                    cls.urls.append(line.strip())
        except IOError as e:
            cls.fail(f"Error reading a file '{file}': {e}")

    def test_novel_titles_from_urls(self):
        """
        Test synchronously fetching novel images from URLs.

        This test iterates over each URL and verifies that the novel image
        can be downloaded and saved successfully using synchronous requests.

        Raises:
            AssertionError: If a novel image is not found for any URL.
        """
        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
            except requests.RequestException as e:
                self.fail(f"Error fetching URL {url}: {e}")
                continue

            page_content = response.content
            soup = BeautifulSoup(page_content, "lxml")
            novel_image_url = get_novel_image_url(url, soup)
            image_path = download_novel_image(
                self.novel_base_url, novel_image_url,
                self.media_dir, "title"
            )
            msg = f"Image not found for URL: {novel_image_url}"

            self.assertNotEqual(image_path, "Not found", msg)

    async def test_async_novel_titles_from_urls(self):
        """
        Test asynchronously fetching novel images from URLs.

        This test iterates over each URL and verifies that the novel image
        can be downloaded and saved successfully using asynchronous requests.

        Raises:
            AssertionError: If a novel image is not found for any URL.
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            for url in self.urls:
                try:
                    async with session.get(url) as response:
                        page_content = await response.text()
                        soup = BeautifulSoup(page_content, "lxml")
                        novel_image_url = get_novel_image_url(url, soup)
                        image_path = await async_download_novel_image(
                            session, self.novel_base_url, novel_image_url,
                            self.media_dir, "title"
                        )
                        msg = f"Image not found for URL: {novel_image_url}"

                        self.assertNotEqual(image_path, "Not found", msg)

                except aiohttp.ClientError as e:
                    self.fail(f"Error fetching URL {url}: {e}")
                    continue


if __name__ == "__main__":
    unittest.main()
