import logging
import os

from dotenv import load_dotenv

load_dotenv()
PATH_TO_LOGS = os.getenv("PATH_TO_LOGS")


def setup_logging(name: str) -> logging.Logger:
    # logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(os.path.join(PATH_TO_LOGS, f"{name}.log"), mode="w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
