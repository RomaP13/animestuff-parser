import unittest

import requests
from bs4 import BeautifulSoup

from utils.novel_utils import get_novel_synopsis


class TestNovelSynopsisExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class variables and read URLs from the input file."""
        filename = "tests/data/urls_with_bugged_synopsises.txt"
        cls.urls = []

        try:
            with open(filename, "r") as file:
                for line in file:
                    cls.urls.append(line.strip())
        except IOError as e:
            cls.fail(f"Error reading a file '{file}': {e}")

    def test_novel_synopsises_from_urls(self):
        """
        Test fetching novel synopsises from URLs in
        urls_with_bugged_synopsises.txt.

        This test iterates over each URL in the file and verifies
        that the novel synopsis can be extracted successfully from the webpage.
        Some URLs may have different HTML structures or formatting, and this
        test ensures that these 'bugged' synopsises can be retrieved.

        Raises:
            AssertionError: If a novel synopsis is not found for any URL.
        """

        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
            except requests.RequestException as e:
                self.fail(f"Error fetching URL {url}: {e}")
                continue

            page_content = response.content
            soup = BeautifulSoup(page_content, "lxml")
            synopsis = get_novel_synopsis(url, soup)
            msg = f"Synopsis not found for URL: {url}"

            self.assertNotEqual(synopsis, "Not found", msg)
            self.assertNotEqual(synopsis, "", msg)


if __name__ == "__main__":
    unittest.main()
