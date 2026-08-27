#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Вказуємо шлях до файлу налаштувань Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # При виконанні команди runserver автоматично перевіряємо підключення БД та створюємо таблиці SQLAlchemy
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        init_sqlalchemy_db()

    execute_from_command_line(sys.argv)


def init_sqlalchemy_db():
    """Ініціалізація та автоматичне створення таблиць SQLAlchemy (за потреби)."""
    try:
        from config.database import engine, Base
        from apps.artworks.models import Artwork, ArtworkStatus
        from apps.users.models import User, UserRole


        # Створення таблиць в PostgreSQL, якщо вони ще не створені
        Base.metadata.create_all(bind=engine)
        print("✅ [SQLAlchemy] Моделі успішно синхронізовані з PostgreSQL.")
    except Exception as e:
        print(f"⚠️ [SQLAlchemy] Помилка при ініціалізації бази даних: {e}")


if __name__ == '__main__':
    main()