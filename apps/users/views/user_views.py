import os
import random
import redis
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from email_validator import validate_email, EmailNotValidError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.serializers import CustomTokenObtainSerializer, AuthenticationSerializer
from core.tasks.emails import send_email

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_ = redis.Redis.from_url(redis_url, decode_responses=True)


@extend_schema(request=AuthenticationSerializer)
@api_view(["POST"])
def send_authentication_code_view(request):
    nums = [str(num) for num in range(10)]
    code = "".join([random.choice(nums) for _ in range(6)])

    authentication_serializer = AuthenticationSerializer(data=request.data)
    authentication_serializer.is_valid(raise_exception=True)
    validated_email = authentication_serializer.validated_data["email"]

    try:
        send_email.delay(
            email_title="authentication code",
            receiver_email=validated_email,
            email_body=f"Your code is {code}",
        )
        redis_.set(f"{validated_email}_code", code, ex=300)
    except Exception as e:
        return Response(data={"detail": f"Error: {e}"})
    return Response(data={"detail": "Email was sent"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def authenticate_user_view(request: Request) -> Response:

    authentication_serializer = AuthenticationSerializer(data=request.data)
    authentication_serializer.is_valid(raise_exception=True)
    validated_email = authentication_serializer.validated_data["email"]
    request_code = request.data.get("code")

    if request_code is None:
        return Response(
            data={"detail: Code field can not be empty"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        validate_email(validated_email, check_deliverability=True)
    except EmailNotValidError as e:
        return Response(
            data={"detail": f"Email is not valid: {e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        saved_code = redis_.get(f"{validated_email}_code")
    except Exception as e:
        return Response(
            data={"detail": f"Redis error: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if saved_code is None:
        return Response(
            data={"detail": "Your code has expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if int(request_code) != int(saved_code):
        return Response(
            data={"detail": "Incorrect code"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        get_user_model().objects.get(email=validated_email)
    except get_user_model().DoesNotExist:
        authentication_serializer.save()

    tokens_serializer = CustomTokenObtainSerializer(data={"email": validated_email})
    if tokens_serializer.is_valid():
        tokens = tokens_serializer.validated_data
    else:
        return Response(
            data=tokens_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    redis_.delete(f"{validated_email}_code")
    return Response(
        data=tokens,
        status=status.HTTP_200_OK,
    )
