import unittest

import requests
from bs4 import BeautifulSoup

from utils.novel_utils import get_novel_title


class TestNovelTitleExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "tests/data/urls_with_bugged_titles.txt"
        cls.urls = []

        try:
            with open(filename, "r") as file:
                for line in file:
                    cls.urls.append(line.strip())
        except IOError as e:
            cls.fail(f"Error reading a file '{file}': {e}")

    def test_novel_titles_from_urls(self):
        """
        Test fetching novel titles from URLs in urls_with_bugged_titles.txt.

        This test iterates over each URL in the file and verifies
        that the novel title can be extracted successfully from the webpage.
        Some URLs may have different HTML structures or formatting, and this
        test ensures that these 'bugged' titles can be retrieved.

        Raises:
            AssertionError: If a novel title is not found for any URL.
        """
        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
            except requests.RequestException as e:
                self.fail(f"Error fetching URL {url}: {e}")
                continue

            page_content = response.content
            soup = BeautifulSoup(page_content, "lxml")
            title = get_novel_title(url, soup)
            msg = f"Title not found for URL: {url}"

            self.assertNotEqual(title, "Not found", msg)


if __name__ == "__main__":
    unittest.main()
