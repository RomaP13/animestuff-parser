import unittest

import requests
from bs4 import BeautifulSoup

from utils.novel_utils import download_novel_image, get_novel_image_url


class TestNovelImageExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
            except requests.RequestException as e:
                self.fail(f"Error fetching URL {url}: {e}")
                continue

            page_content = response.content
            soup = BeautifulSoup(page_content, "lxml")
            novel_image_url = get_novel_image_url(url, soup)
            image_path = download_novel_image(self.novel_base_url,
                                              novel_image_url, self.media_dir,
                                              "title")
            msg = f"Image not found for URL: {novel_image_url}"

            self.assertNotEqual(image_path, "Not found", msg)


if __name__ == "__main__":
    unittest.main()
