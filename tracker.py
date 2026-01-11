import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

PRODUCT_ID = "20210725"
URL = f"https://www.zara.com/tr/tr/products-details?productIds={PRODUCT_ID}"
STATE_FILE = "last.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "tr-TR,tr;q=0.9"
}

def get_stock_status():
    url = "https://www.zara.com/tr/tr/products-details"
    params = {
        "productIds": PRODUCT_ID,
        "ajax": "true",
        "channel": "mobile",
        "deviceType": "PHONE"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7)",
        "Accept": "application/json",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "Referer": f"https://www.zara.com/tr/tr/p{PRODUCT_ID}.html"
    }

    r = requests.get(url, params=params, headers=headers, timeout=20)
    r.raise_for_status()

    data = r.json()

    print("DEBUG API RESPONSE:", data)

    if not data or not isinstance(data, list):
        return "Stok Yok"

    product = data[0]

    for size in product.get("sizes", []):
        if size.get("availability") in ("in_stock", "AVAILABLE"):
            return "Stokta"

    return "Stok Yok"




def load_last_stock():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("stock", "Stok Yok")
    except:
        return "Stok Yok"

def save_stock(stock):
    with open(STATE_FILE, "w") as f:
        json.dump({"stock": stock}, f, indent=2)

def send_mail():
    sender = os.environ["MAIL_USER"]
    password = os.environ["MAIL_PASS"]
    receiver = os.environ["MAIL_TO"]

    body = f"""
ZARA Ürün Stokta!

Ürün tekrar satışa açıldı.

Link:
https://www.zara.com/tr/tr/p{PRODUCT_ID}.html

Tarih:
{datetime.now()}
"""

    msg = MIMEText(body)
    msg["Subject"] = "ZARA Ürün Stokta!"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def main():
    current_stock = get_stock_status()
    last_stock = load_last_stock()

    print("Önceki stok:", last_stock)
    print("Şu anki stok:", current_stock)

    if last_stock == "Stok Yok" and current_stock == "Stokta":
        send_mail()

    save_stock(current_stock)

if __name__ == "__main__":
    main()
