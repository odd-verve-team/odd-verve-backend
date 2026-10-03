import os
import resend
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
resend_api_key = os.getenv("RESEND_API_KEY")

resend.api_key = resend_api_key

app = Celery("emails", broker=redis_url, backend=redis_url)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, email_title: str, receiver_email: str, email_body: str) -> None:
    try:
        params: resend.Emails.SendParams = {
            "from": "Acme",
            "to": [receiver_email],
            "subject": email_title,
            "html": email_body
        }
        resend.Emails.send(params)
    except Exception as error:
        raise self.retry(exc=error)
