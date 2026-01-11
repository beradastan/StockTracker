import json
import os

LAST_FILE = "last.json"
MAX_MAIL = 3


def load_state():
    if not os.path.exists(LAST_FILE):
        return {}
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def can_send_mail(url):
    state = load_state()
    count = state.get(url, 0)

    if count >= MAX_MAIL:
        return False

    state[url] = count + 1
    save_state(state)
    return True
