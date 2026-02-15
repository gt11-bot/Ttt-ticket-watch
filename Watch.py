
import requests
from bs4 import BeautifulSoup
import os

# Seurattava sivu
URL = "https://ttt-teatteri.fi/program/kaunotar-ja-hirvio/#esityskalenteri"

# Telegram bot token ja chat id
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Tiedosto jossa viimeisin tila
STATE_FILE = "state.txt"


def page_has_available():
    """Tarkistaa onko sivulla teksti 'täyttymässä'"""
    response = requests.get(URL, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()
    return "täyttymässä" in text


def send_telegram(message):
    """Lähettää viestin Telegramiin"""
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )


def read_last_state():
    """Lue viimeisin tila state.txt:stä"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return "none"


def save_state(state):
    """Tallenna tila state.txt:ään"""
    with open(STATE_FILE, "w") as f:
        f.write(state)


# Päälogiikka
current_available = page_has_available()
last_state = read_last_state()

# Jos löytyy 'täyttymässä' eikä ole jo ilmoitettu
if current_available and last_state != "available":
    send_telegram("🎟️ Jossain esityksessä näkyy teksti 'Täyttymässä'!")
    save_state("available")

# Jos ei enää 'täyttymässä' → nollataan tila
elif not current_available:
    save_state("none")
