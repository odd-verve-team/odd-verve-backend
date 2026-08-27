import sys
from .base import *

DEBUG = True

# Якщо запускаються тести — використовуємо кеш в пам'яті замість Redis
if 'pytest' in sys.modules or 'test' in sys.argv:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    
ALLOWED_HOSTS = ['*']

# SQL Логування в консоль для відладки SQLAlchemy
SQL_ECHO = True

# Можна перевизначити CORS для будь-якого домену на локалці
CORS_ALLOW_ALL_ORIGINS = True