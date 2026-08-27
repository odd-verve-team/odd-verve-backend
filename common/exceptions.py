from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class APIException(Exception):
    """
    Базовий виняток для застосунку з можливістю вказувати HTTP статус-код.
    """
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, code: str = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code or "BAD_REQUEST"


class NotFoundException(APIException):
    def __init__(self, message: str = "Запитуваний ресурс не знайдено"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, code="NOT_FOUND")


class UnauthorizedException(APIException):
    def __init__(self, message: str = "Необхідна автентифікація"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, code="UNAUTHORIZED")


class ForbiddenException(APIException):
    def __init__(self, message: str = "Доступ заборонено"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN, code="FORBIDDEN")


class InsufficientStockException(APIException):
    def __init__(self, message: str = "Товару / картини немає в наявності"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT, code="OUT_OF_STOCK")


def custom_exception_handler(exc, context):
    """
    Глобальний обробник помилок Django REST Framework & Кастомних APIException.
    Перетворює помилки в єдиний формат JSON-відповіді.
    """
    # Обробка власних кастомних винятків
    if isinstance(exc, APIException):
        return Response(
            {
                "error": {
                    "code": exc.code,
                    "message": exc.message
                }
            },
            status=exc.status_code
        )

    # Обробка стандартних помилок DRF (Validation, NotFound і т.д.)
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "error": {
                "code": "VALIDATION_ERROR" if response.status_code == 400 else "API_ERROR",
                "message": response.data.get("detail", response.data)
            }
        }
        response.data = custom_data
        return response

    # Якщо помилка не перехоплена (наприклад, Unhandled 500 Server Error)
    logger.error(f"Необроблена помилка сервера: {exc}", exc_info=True)
    return Response(
        {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Сталася внутрішня помилка сервера. Спробуйте пізніше."
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )