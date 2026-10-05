import os
import yagmail
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
resend_api_key = os.getenv("RESEND_API_KEY")

resend.api_key = resend_api_key

app = Celery("emails", broker=redis_url, backend=redis_url)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, email_title: str, receiver_email: str, email_body: str) -> None:
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_EMAIL_PASSWORD")
    try:
        with yagmail.SMTP(user=sender_email, password=sender_password) as yag:
            yag.send(
                to=receiver_email,
                subject=email_title,
                contents=email_body
            )
    except Exception as error:
        raise self.retry(exc=error)