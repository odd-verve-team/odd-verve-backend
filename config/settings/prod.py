from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Безпека для Cookies у продакшн (HTTPS)
JWT_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Перевірка на використання секретних ключів
if SECRET_KEY == "django-insecure-change-me-in-production":
    raise ValueError("Увага! Необхідно встановити SECRET_KEY у зміних середовища (.env) для production!")