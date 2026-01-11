import json
import os

LAST_FILE = "last.json"
MAX_MAIL = 3


def load_last():
    if not os.path.exists(LAST_FILE):
        return {}
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_last(data):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def can_send_mail(url):
    data = load_last()
    return data.get(url, 0) < MAX_MAIL


def mark_mail_sent(url):
    data = load_last()
    data[url] = data.get(url, 0) + 1
    save_last(data)


def reset_mail_counter(url):
    data = load_last()
    if url in data:
        del data[url]
        save_last(data)
