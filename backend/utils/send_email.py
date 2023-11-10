import os
import smtplib, ssl
from dotenv import load_dotenv

load_dotenv()

port = int(os.getenv("SMTP_PORT"))


def send_email(sender_email, receiver_email, message):
    if sender_email is None or receiver_email is None or message is None:
        raise AssertionError("Invalid email parameters")
    with smtplib.SMTP(os.getenv("SMTP_SERVER"), port) as server:
        server.sendmail(sender_email, receiver_email, message)
