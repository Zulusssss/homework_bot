import logging
import requests
import telegram
import time
import os
from dotenv import load_dotenv

from handlers import TelegramHandler
from logging.handlers import RotatingFileHandler

load_dotenv()


def setup_logs():
    """Устанавливает логи для бота."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        filename='homework_DEBUG.log',
        filemode='w',
        level=logging.DEBUG,
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    file_handler = RotatingFileHandler(
        'my_logger.log',
        maxBytes=50000000,
        backupCount=5
    )
    telegram_handler = TelegramHandler(level='ERROR')
    formater = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formater)

    telegram_handler.setLevel(logging.ERROR)
    telegram_handler.setFormatter(formater)

    logger.addHandler(file_handler)
    logger.addHandler(telegram_handler)

    return logger


logger = setup_logs()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяет наличие всех необходимых токенов."""
    if not(PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
        logging.critical('отсутствие обязательных переменных '
                         'окружения во время запуска бота')
    return (PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID)


def send_message(bot, message):
    """Отправляет сообщение в чат с ботом от бота."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
    except telegram.error.TelegramError:
        logger.error('сбой при отправке сообщения в Telegram')
    else:
        logging.debug('удачная отправка любого сообщения в Telegram')


def get_api_answer(timestamp):
    """Осуществляет запрос к API."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
        if response.status_code == 200 and check_response(response.json()):
            return response.json()
        else:
            logger.error('Плохое соединение с API')
            raise Exception('Плохое соединение с API')

    except requests.RequestException as e:
        logger.error("недоступность эндпоинта или сбои "
                     f"при запросе к нему: {e}")


def check_response(response):
    """Проверяет соответствие ответа API документации API."""
    if type(response) is not dict:
        raise TypeError('Неподходящий тип данных ответа API - не словарь')
    if type(response.get('homeworks')) is not list:
        raise TypeError('Неподходящий тип данных ответа API - не cписок')
    if list(response.keys()) == ['homeworks', 'current_date']:
        return True
    else:
        logger.error('отсутствие ожидаемых ключей в ответе API')
        return False


def parse_status(homework):
    """
    Возвращает строку для отправки ботом в чат.
    Запускается, когда статус домашней работы изменился.
    """
    if 'homework_name' not in homework.keys():
        logger('в ответе API домашки нет ключа `homework_name')
        raise KeyError('в ответе API домашки нет ключа `homework_name')
    if homework.get('status') not in HOMEWORK_VERDICTS.keys():
        logger.error('неожиданный статус домашней работы, '
                     'обнаруженный в ответе API')
        raise KeyError(f"KeyError('{homework.get('status')}')")

    homework_name = homework.get('homework_name')
    verdict = HOMEWORK_VERDICTS[homework.get('status')]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    response = None
    while True:
        if not(check_tokens()):
            break
        try:
            response = get_api_answer(timestamp)
            homeworks = response.get('homeworks')
            if len(homeworks) > 0:
                homework = homeworks[0]
                send_message(bot, parse_status(homework))
            else:
                logging.debug('отсутствие в ответе новых статусов')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        finally:
            if response is not None:
                timestamp = response.get('current_date')
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
