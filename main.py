import os
import requests
from time import sleep
import telegram
import textwrap


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
        print("Connection error")
        sleep(10)
    except requests.exceptions.HTTPError:
        print(f"Http error: {long_polling_url}")
        sleep(30)


def start_bot():
    dvmn_token = os.environ['DVMN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']

    bot = telegram.Bot(token=telegram_token)

    timestamp_to_request = None

    while True:
        reviews = get_long_polling_reviews(timestamp=timestamp_to_request, token=dvmn_token)
        print(reviews)
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
    start_bot()