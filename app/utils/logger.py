import logging
from logging.handlers import RotatingFileHandler
import os


BASE_DIR = "logs"
FILENAME = "app.log"
LOG_PATH = os.path.join(BASE_DIR, FILENAME)

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

logging.basicConfig(
    filemode="a",
    format="[%(levelname)s] %(asctime)s: %(message)s",
    level=logging.DEBUG,
)

rotate_handler = RotatingFileHandler(LOG_PATH, maxBytes=2000, backupCount=5)
logger = logging.getLogger("app")
logger.addHandler(rotate_handler)