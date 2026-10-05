import os
import requests
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
sender_email = os.environ.get("SENDER_EMAIL")
sender_password = os.environ.get("SENDER_EMAIL_PASSWORD")
api_key = os.environ.get("MAILGUN_API_KEY")

app = Celery("emails", broker=redis_url, backend=redis_url)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, email_title: str, receiver_email: str, email_body: str) -> None:
    try:
        response = requests.post(
            "https://api.mailgun.net/v3/sandbox48011dc62c304c809b9e8a95a2b3c0dc.mailgun.org/messages",
            auth=("api", api_key),
            data={
                "from": sender_email,
                "to": receiver_email,
                "subject": email_title,
                "text": email_body,
            },
        )
        response.raise_for_status()
    except Exception as error:
        raise self.retry(exc=error)
