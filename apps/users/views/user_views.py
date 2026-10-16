import os
import secrets
import logging
import redis
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from email_validator import validate_email, EmailNotValidError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.serializers import (
    CustomTokenObtainSerializer,
    AuthenticationSerializer,
    UserSerializer,
)
from core.tasks.emails import send_email

logger = logging.getLogger(__name__)
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_ = redis.Redis.from_url(redis_url, decode_responses=True)


@extend_schema(request=AuthenticationSerializer)
@api_view(["POST"])
def send_authentication_code_view(request):
    nums = [str(num) for num in range(10)]
    code = "".join([secrets.choice(nums) for _ in range(6)])

    authentication_serializer = AuthenticationSerializer(data=request.data)
    authentication_serializer.is_valid(raise_exception=True)
    validated_email = authentication_serializer.validated_data["email"]

    try:
        redis_.set(f"{validated_email}_code", code, ex=300)
        send_email.delay(
            email_title="Authentication code",
            receiver_email=validated_email,
            email_body=f"Your code is: {code}",
        )
    except Exception as e:
        logger.exception(
            f"An error occurred during creating authentication code and sending an email: {e}"
        )
        return Response(
            data={"detail": "Server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(data={"detail": "Email was sent"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def authenticate_user_view(request: Request) -> Response:
    request_email = request.data.get("email")
    request_code = request.data.get("code")

    if request_email is None or request_code is None:
        return Response(
            data={"detail": "Code or email fields can not be empty"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    authentication_serializer = AuthenticationSerializer(data=request.data)
    authentication_serializer.is_valid(raise_exception=True)
    validated_email = authentication_serializer.validated_data["email"]

    try:
        saved_code = redis_.get(f"{validated_email}_code")
    except Exception as e:
        logger.exception(f"An error occurred when obtaining user's redis code: {e}")
        return Response(
            data={"detail": "Server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if saved_code is None:
        return Response(
            data={"detail": "Your code has expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if str(request_code) != str(saved_code):
        return Response(
            data={"detail": "Incorrect code"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = get_user_model().objects.get(email=validated_email)
    except get_user_model().DoesNotExist:
        authentication_serializer.save()
        user = get_user_model().objects.get(email=validated_email)

    user_serializer = UserSerializer(user)
    serialized_user = user_serializer.data
    tokens_serializer = CustomTokenObtainSerializer(data={"email": validated_email})
    tokens_serializer.is_valid(raise_exception=True)
    tokens = tokens_serializer.validated_data
    redis_.delete(f"{validated_email}_code")
    return Response(
        data={"tokens": tokens, "user": serialized_user},
        status=status.HTTP_200_OK,
    )
