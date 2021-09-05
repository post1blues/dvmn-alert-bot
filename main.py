import os
import requests
from time import sleep
import telegram
import textwrap
import logging


def get_long_polling_reviews(timestamp, token):
    request_timeout = 100
    long_polling_url = "https://dvmn.org/api/long_polling/"
    payload = {"timestamp": timestamp}
    headers = {"Authorization": f"Token {token}"}

    try:
        response = requests.get(
            long_polling_url,
            headers=headers,
            params=payload,
            timeout=request_timeout
        )
        response.raise_for_status()
        print(response.url)
        return response.json()
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
        sleep(10)
    except requests.exceptions.HTTPError:
        sleep(30)


def start_bot():
    timestamp_to_request = None

    while True:
        reviews = get_long_polling_reviews(timestamp=timestamp_to_request, token=dvmn_token)
        if reviews["status"] == "timeout":
            timestamp_to_request = reviews["timestamp_to_request"]
        else:
            timestamp_to_request = reviews["last_attempt_timestamp"]

            for new_attempt in reviews["new_attempts"]:
                lesson_title = new_attempt["lesson_title"]

                if new_attempt["is_negative"]:
                    status = "К сожалению в работе нашлись ошибки и нужно немного доработать."
                else:
                    status = "Преподавателю все понравилось, можно приступать к следующему уроку."

                message = f"""\
                Преподаватель проверил работу "{lesson_title}"!
                {status}
                Ссылка на урок: https://dvmn.org{new_attempt['lesson_url']}
                """

                bot.send_message(chat_id=chat_id, text=textwrap.dedent(message))


if __name__ == "__main__":
    dvmn_token = os.environ["DVMN_TOKEN"]
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["CHAT_ID"]

    logging.basicConfig(format="%(levelname)s %(message)s")

    class TelegramLogsHandler(logging.Handler):

        def __init__(self, log_chat_id):
            super().__init__()
            self.log_chat_id = log_chat_id
            self.tg_bot = telegram.Bot(token=telegram_token)

        def emit(self, record):
            log_entry = self.format(record)
            self.tg_bot.send_message(chat_id=self.log_chat_id, text=log_entry)

    logger = logging.getLogger("Logger")
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(chat_id))

    while True:
        try:
            logger.warning("Bot starts working")
            bot = telegram.Bot(token=telegram_token)
            start_bot()
        except Exception as error:
            error_msg = f"""\
            Bot failed.
            {error}

            Try to restart the bot.
            """
            
            logger.error(textwrap.dedent(error_msg))
