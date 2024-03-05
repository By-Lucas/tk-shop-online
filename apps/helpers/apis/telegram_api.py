import os
import requests
import mimetypes
#from dotenv import load_dotenv
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from config.models.models_telegram import AuthTelegramModel

# from requests.packages.urllib3.util.retry import Retry


TELEGRAM_API_URL = ""

# retry_strategy = Retry(
#     connect=3,
#     total=3,
#     backoff_factor=1,
#     status_forcelist=[429, 500, 502, 503, 504, 104, 403],
#     method_whitelist=["HEAD", "POST", "PUT", "GET", "OPTIONS"]
# )

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504, 104, 403],
    allowed_methods=["HEAD", "POST", "PUT", "GET", "OPTIONS"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)


class Browser(object):

    def __init__(self):
        self.response = None
        self.headers = None
        self.session = requests.Session()

    def set_headers(self, headers=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36"
        }
        if headers:
            for key, value in headers.items():
                self.headers[key] = value

    def get_headers(self):
        return self.headers

    def send_request(self, method, url, **kwargs):
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        return self.session.request(method, url, **kwargs)


def escape_telegrambot_underscore(txt):
    return txt.replace(" " * 4, "") \
        .replace("_", f"_") \
        .replace("-", f"-") \
        .replace("~", f"~") \
        .replace("`", f"`") \
        .replace(".", f".")


def send_photo_with_description(photo_path, chat_id, description, parse_mode=None, notify=True):
    global TELEGRAM_API_URL
    
    auth_telegram = AuthTelegramModel.objects.first()
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{auth_telegram.bot_token}/"
    browser = Browser()
    with open(photo_path, 'rb') as photo_file:
        payload = {
            'chat_id': chat_id,
            'caption': description,
            'parse_mode': parse_mode,
            'disable_notification': not notify
        }
        response = browser.send_request(
            method="POST",
            url=f"{TELEGRAM_API_URL}sendPhoto",
            data=payload,
            files={"photo": photo_file}
        )

        result = response.json()
        if result.get("ok"):
            return result

        return None

def send_media_with_description(media_path, chat_id, description, parse_mode="Markdown", notify=True) -> dict:
    "Enviar Imagem/Video + descrição"
    global TELEGRAM_API_URL
    
    auth_telegram = AuthTelegramModel.objects.first()
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{auth_telegram.bot_token}/"
    
    browser = Browser()
    media_type = mimetypes.guess_type(media_path)[0]

    if media_type and media_type.startswith("image"):
        # É uma imagem
        with open(media_path, 'rb') as media_file:
            payload = {
                'chat_id': chat_id,
                'caption': description,
                'parse_mode': parse_mode,
                'disable_notification': not notify
            }
            response = browser.send_request(
                method="POST",
                url=f"{TELEGRAM_API_URL}sendPhoto",
                data=payload,
                files={"photo": media_file}
            )

            result = response.json()
            if result.get("ok"):
                return result

    elif media_type and media_type.startswith("video"):
        # É um vídeo
        with open(media_path, 'rb') as media_file:
            payload = {
                'chat_id': chat_id,
                'caption': description,
                'parse_mode': parse_mode,
                'disable_notification': not notify
            }
            response = browser.send_request(
                method="POST",
                url=f"{TELEGRAM_API_URL}sendVideo",
                data=payload,
                files={"video": media_file}
            )

            result = response.json()
            if result.get("ok"):
                return result

    return None