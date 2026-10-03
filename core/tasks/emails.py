import os
import smtplib
import random
from email.message import EmailMessage

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("emails", broker=redis_url, backend=redis_url)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, email_title: str, receiver_email: str, email_body: str) -> None:
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_EMAIL_PASSWORD")

    email = EmailMessage()
    email["Subject"] = email_title
    email["From"] = sender_email
    email["To"] = receiver_email
    email.set_content(email_body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(email)
    except Exception as error:
        raise self.retry(exc=error)
