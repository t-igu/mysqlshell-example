import sys
from loguru import logger

def setup_logger(logfile_path, rotation="1 days", retention="10 days"):

    config = {
        "handlers": [
            {"sink": sys.stdout},
            {"sink": logfile_path, "rotation": rotation, "retention": retention},
        ],
    }
    logger.configure(**config)