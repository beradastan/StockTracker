import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

load_dotenv()

def send_mail(product_url):
    sender = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASS")
    receiver = os.getenv("MAIL_TO")

    if not all([sender, password, receiver]):
        raise RuntimeError("Missing MAIL configuration! (Check your .env file)")

    body = f"""
 ÜRÜN STOKTA 🚨

Aşağıdaki ürün stokta görünüyor:

{product_url}

Tarih:
{datetime.now()}
"""

    msg = MIMEText(body)
    msg["Subject"] = "Ürün Stokta!"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
