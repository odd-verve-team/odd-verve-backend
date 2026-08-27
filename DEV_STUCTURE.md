# Структура проекта

```text
backend/
├── config/              # Налаштування Django (settings, urls, wsgi/asgi)
│   ├── settings/        # Налаштування (base.py, local.py, prod.py)
│   ├── urls.py          # Головний роутер API
│   └── database.py      # Налаштування підключення SQLAlchemy Engine & Sessions
├── apps/                # Django-додатки (модулі бізнес-логіки)
│   ├── authentication/  # Авторизація (JWT, HttpOnly Cookies)
│   ├── users/           # Управління профілями
│   ├── artworks/        # Каталог картин, категорій та медіа
│   ├── cart/            # Кошик (Redis + БД)
│   └── orders/          # Оформлення замовлень та оплата
├── common/              # Спільний функціонал
│   ├── permissions.py   # Кастомні перевірки прав доступу
│   ├── utils_s3.py      # Хелпери для завантаження в AWS S3 / Cloudinary
│   └── exceptions.py    # Глобальна обробка помилок
├── media/               # Медіафайли у режимі розробки
├── tests/               # Тестування
├── docker-compose.yml   # Контейнеризація (Django, PostgreSQL, Redis)
├── requirements.txt
└── manage.py
```

<!--
## Поточний стан

- Синхроні запити
- Тестування синхроне

## Tasks

- Переродити запити у асинхроні
- Переробити тести

-->

## Скріни находятся у папці `media/`
