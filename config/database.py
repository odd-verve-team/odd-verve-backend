import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker #, scoped_session

# Атмосферні змінні або значення за замовчуванням
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "art_gallery_db")

# Беремо параметри з змінних середовища або налаштувань
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Створення Engine та Сесії
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Автоматична перевірка з'єднання
    echo=os.getenv("SQL_ECHO", "False").lower() in ("true", "1")
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Базовий клас для всіх моделей SQLAlchemy
Base = declarative_base()

def get_db():
    """Генератор сесій SQLAlchemy для передачі у Views / Services"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()