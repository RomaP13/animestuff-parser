import logging
import unittest

import requests
from bs4 import BeautifulSoup

from utils.novel_utils import (get_novel_genres, get_novel_status,
                               get_novel_synopsis, get_novel_title,
                               get_number_of_volumes)


class TestNovelUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "tests/data/urls_test_cases.txt"
        cls.urls = []
        cls.page_contents = {}
        try:
            with open(filename, "r") as file:
                for line in file:
                    url = line.strip()
                    cls.urls.append(url)
                    cls.page_contents[url] = cls.fetch_page_content(url)
        except IOError as e:
            raise Exception(f"Error reading a file '{file}': {e}")

        # Set logging level to ERROR to suppress warnings and
        # info messages during tests
        logging.basicConfig(level=logging.ERROR)

    @staticmethod
    def fetch_page_content(url: str):
        try:
            response = requests.get(url, timeout=10)
            return response.content
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    def test_get_novel_title(self):
        """
        Test extracting novel titles from URLs in urls_test_cases.txt.

        This test iterates over each URL in the file and verifies
        that the novel title can be extracted successfully from the webpage.

        Raises:
            AssertionError: If a novel title is not found for any URL.
        """
        for url in self.urls:
            page_content = self.page_contents.get(url)
            if page_content:
                soup = BeautifulSoup(page_content, "lxml")
                title = get_novel_title(url, soup)
                msg = f"Title not found for URL: {url}"

                self.assertNotEqual(title, "Not found", msg)

    def test_get_novel_status(self):
        """
        Test extracting novel status from URLs in urls_test_cases.txt.

        This test iterates over each URL in the file and verifies
        that the novel status can be extracted successfully from the webpage.

        Raises:
            AssertionError: If a novel status is not found for any URL.
        """
        for url in self.urls:
            page_content = self.page_contents.get(url)
            if page_content:
                soup = BeautifulSoup(page_content, "lxml")
                status = get_novel_status(url, soup)
                msg = f"Status not found for URL: {url}"

                self.assertNotEqual(status, "Not found", msg)

    def test_get_novel_synopsis(self):
        """
        Test extracting novel synopsis from URLs in urls_test_cases.txt.

        This test iterates over each URL in the file and verifies
        that the novel synopsis can be extracted successfully from the webpage.

        Raises:
            AssertionError: If a novel synopsis is not found for any URL.
        """
        for url in self.urls:
            page_content = self.page_contents.get(url)
            if page_content:
                soup = BeautifulSoup(page_content, "lxml")
                synopsis = get_novel_synopsis(url, soup)
                msg = f"Synopsis not found for URL: {url}"

                self.assertNotEqual(synopsis, "Not found", msg)

    def test_get_novel_genres(self):
        """
        Test extracting novel genres from URLs in urls_test_cases.txt.

        This test iterates over each URL in the file and verifies
        that the novel genres can be extracted successfully from the webpage.

        Raises:
            AssertionError: If a novel genres are not found for any URL.
        """
        for url in self.urls:
            page_content = self.page_contents.get(url)
            if page_content:
                soup = BeautifulSoup(page_content, "lxml")
                genres = get_novel_genres(url, soup)
                msg = f"Genres not found for URL: {url}"

                self.assertNotEqual(genres, "Not found", msg)

    def test_get_number_of_volumes(self):
        """
        Test extracting number of volumes of a novel from URLs
        in urls_test_cases.txt.

        This test iterates over each URL in the file and verifies
        that the number of volumes can be extracted successfully from
        the webpage.

        Raises:
            AssertionError: If the number of volumes is 0 for any URL.
        """
        for url in self.urls:
            page_content = self.page_contents.get(url)
            if page_content:
                soup = BeautifulSoup(page_content, "lxml")
                num_volumes = get_number_of_volumes(url, soup)
                msg = f"Number of volumes not found for URL: {url}"

                self.assertNotEqual(num_volumes, 0, msg)


if __name__ == "__main__":
    unittest.main()
