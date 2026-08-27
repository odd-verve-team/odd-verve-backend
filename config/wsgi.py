import os
from django.core.wsgi import get_wsgi_application

# Вказуємо шлях до налаштувань за замовчуванням
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = get_wsgi_application()