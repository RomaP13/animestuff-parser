from modules.logging_config import setup_logging
from modules.novel_parser import (download_novel_html_files, get_all_novels,
                                  get_data_from_html_files)


def main() -> None:
    WEBSITE_BASE_URL = "https://animestuff.me/"
    NOVEL_BASE_URL = "https://animestuff.me/docs/assets/html/"
    NOVELS_FILE = "all_novels_dict.json"
    DIRECTORY = "html_files"
    DATA_FILE = "data.json"

    get_all_novels(WEBSITE_BASE_URL, NOVEL_BASE_URL, NOVELS_FILE)
    download_novel_html_files(NOVELS_FILE, DIRECTORY)
    get_data_from_html_files(DIRECTORY, NOVELS_FILE, DATA_FILE)


if __name__ == "__main__":
    setup_logging()
    main()
