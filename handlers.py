import logging

import telegram

import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

TOKENS = dict(dotenv_values('.env'))
values = (x for x in TOKENS.values())
for i in TOKENS.keys():
    exec('%s = next(values)' % i, globals())
del(i)

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
        if message.find('ERROR') != -1:
            text_message = message.split('ERROR', 1)[1].lstrip()
            text_message = text_message.split('Traceback', 1)[0].rstrip()
            if self.pre_message != text_message:
                self.send_message(message.split('Traceback', 1)[0].rstrip())
                self.pre_message = text_message
        else:
            return None
