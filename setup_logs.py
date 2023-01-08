import logging
import sys
from handlers import TelegramHandler
from logging.handlers import RotatingFileHandler

def setup_logs():
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        filename='homework_DEBUG.log',
        filemode='w',
        level=logging.DEBUG,
        )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    # console_handler = logging.StreamHandler(stream=sys.stdout)
    file_handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5, exc_info=True)
    telegram_handler = TelegramHandler()
    formater = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # console_handler.setLevel(logging.ERROR)
    # console_handler.setFormatter(formater)

    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formater)

    telegram_handler.setLevel(logging.ERROR)
    telegram_handler.setFormatter(formater)

    # logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(telegram_handler)

    return logger