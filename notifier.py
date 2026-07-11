import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def _smtp_send(subject: str, body: str):
    sender = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASS")
    receivers = [
        mail.strip()
        for mail in os.getenv("MAIL_TO", "").split(",")
        if mail.strip()
    ]

    if not all([sender, password, receivers]):
        raise RuntimeError("Missing MAIL configuration! (Check GitHub Secrets / env vars)")

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())

def send_stock_mail(product_url: str, extra: str = ""):
    body = (
        "ÜRÜN STOKTA🚨\n\n"
        "Aşağıdaki ürün stokta görünüyor:\n\n"
        f"{product_url}\n"
    )

    if extra.strip():
        body += f"\nDetay:\n{extra}\n"

    body += f"\nTarih:\n{datetime.now()}\n"
    _smtp_send("Ürün Stokta Aşkım!", body)

def send_startup_mail(products: dict):
    lines = ["🟢 Stock Tracker BAŞLADI", "", "Takip edilen ürünler:"]
    for brand, items in products.items():
        lines.append(f"\n🔹 {brand.upper()}")
        for p in items:
            sizes = p.get("sizes", [])
            size_txt = f" (Bedenler: {', '.join(sizes)})" if sizes else " (Beden: tüm/tek varyant)"
            lines.append(f"- {p.get('url')}{size_txt}")

    body = "\n".join(lines) + f"\n\nTarih:\n{datetime.now()}\n"
    _smtp_send("Stock Tracker Başladı", body)
