import logging
import os
from datetime import datetime


def setup_logging():
    # Create the logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Generate a log file name with the current date and time
    log_filename = datetime.now().strftime('logs/%Y-%m-%d_%H-%M-%S.log')

    # Configure the logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        handlers=[
            # Direct logs to the date-time-named log file
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also output logs to the console
        ]
    )
