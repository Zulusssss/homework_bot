import logging

import telegram

import os
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = telegram.Bot(token=TELEGRAM_TOKEN)


class TelegramHandler(logging.Handler):
    def __init__(self, level):
        super().__init__(level)
        self.pre_message = None

    def send_message(self, message):
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )

    def emit(self, record):
        message = self.format(record)
        text_message = message.split('ERROR', 1)[1].lstrip()
        if self.pre_message == text_message:
            return None
        else:
            self.send_message(message)
            self.pre_message = text_message
