import os

from modules.logging_config import setup_logging
from modules.novel_parser import (download_novel_html_files, get_all_novels,
                                  get_data_from_html_files)


def main() -> None:
    WEBSITE_BASE_URL = "https://animestuff.me/"
    NOVEL_BASE_URL = "https://animestuff.me/docs/assets/html/"
    HTML_FILES_DIR = "html_files"
    MEDIA_DIR = "static/media"
    DATA_DIR = "data"
    DATA_FILE = os.path.join(DATA_DIR, "novels_data.json")
    NOVELS_FILE = os.path.join(DATA_DIR, "all_novels_dict.json")

    # Create necessary directories
    os.makedirs(HTML_FILES_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    get_all_novels(WEBSITE_BASE_URL, NOVEL_BASE_URL, NOVELS_FILE)
    download_novel_html_files(NOVELS_FILE, HTML_FILES_DIR)
    get_data_from_html_files(NOVEL_BASE_URL, HTML_FILES_DIR, MEDIA_DIR,
                             NOVELS_FILE, DATA_FILE)


if __name__ == "__main__":
    setup_logging()
    main()
