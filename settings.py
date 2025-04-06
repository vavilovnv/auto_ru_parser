import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    CSV_FOLDER_NAME: str = "csv_files"
    URL: str = os.getenv("URL")
    COOKIE: str = os.getenv("COOKIE")
    HEADERS: dict[str, str] = {
        "user-agent": os.getenv("USER_AGENT"),
        "accept": os.getenv("ACCEPT"),
        "Accept-Language": "ru",
        "accept-encoding": "accept - encoding: gzip, deflate, br",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Opera";v="87"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "Cookie": COOKIE,
    }
    OPEN_CSV_FILE: bool = True


app_settings = Settings()
