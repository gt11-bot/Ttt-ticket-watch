import requests
from bs4 import BeautifulSoup
import os

URL = "https://ttt-teatteri.fi/program/kaunotar-ja-hirvio/#esityskalenteri"
TARGET_DATE = "9.4"

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def notify(message):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message}
    )


def check_page():
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    page_text = soup.get_text(separator="\n").lower()
    lines = page_text.split("\n")

    for line in lines:
        if TARGET_DATE in line:
            if "täyttymässä" in line:
                notify("🎟️ 9.4 esitykseen vapautui lippuja!")
            return


if __name__ == "__main__":
    check_page()
