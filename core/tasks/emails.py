import os
import smtplib
from email.message import EmailMessage
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
sender_email = os.environ.get("SENDER_EMAIL")
sender_password = os.environ.get("SENDER_PASSWORD")

app = Celery("emails", broker=redis_url, backend=redis_url)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, email_title: str, receiver_email: str, email_body: str) -> None:
    email = EmailMessage()
    email["To"] = receiver_email
    email["Subject"] = email_title
    email["From"] = sender_email
    email.set_content(email_body)

    try:
       with smtplib.SMTP("smtp.gmail.com", 587) as server:
           server.starttls()
           server.login(sender_email, sender_password)
           server.send_message(email)
    except Exception as error:
        raise self.retry(exc=error)
