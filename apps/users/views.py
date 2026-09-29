import os
import random
import redis
import requests
from email_validator import validate_email, EmailNotValidError
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserRegisterSerializer,
)
from core.tasks.emails import send_email


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all().prefetch_related("artworks")


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all().prefetch_related("artworks")


@api_view(["POST"])
def send_authentication_email_code_view(request):
    nums = [str(num) for num in range(10)]
    code = "".join([random.choice(nums) for _ in range(7)])

    receiver_email = request.data.get("email")

    if not receiver_email:
        return Response(
            data={"Error": "Email can not be empty"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_email(receiver_email, check_deliverability=True)
    except EmailNotValidError as e:
        return Response(
            data={"Error": f"Email is invalid: {e}"}, status=status.HTTP_400_BAD_REQUEST
        )

    send_email.delay(
        email_title="Email code",
        receiver_email=receiver_email,
        email_body=f"Your code is {code}",
    )

    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_ = redis.Redis.from_url(redis_url, decode_responses=True)
    redis_.set(f"{receiver_email}_code", code, ex=300)

    return Response(data="Email was sent", status=status.HTTP_200_OK)


@api_view(["POST"])
def authenticate_user_view(request):
    email = request.data.get("email")
    input_code = request.data.get("code")

    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_ = redis.Redis.from_url(redis_url, decode_responses=True)
    saved_code = redis_.get(f"{email}_code")
    if saved_code is None:
        return Response(
            data={"Error": "Your code has expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if input_code != saved_code:
        return Response(
            data={"Error": "Incorrect code"}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        user = User.objects.filter(email=email)
        if user:
            response = requests.post(
                url="https://odd-verve-backend.onrender.com/token/",
                json={
                    "email": user.email,
                },
            )
            if response.status_code == 200:
                jwt_tokens = response.json()
                access_token = jwt_tokens["access_token"]
                refresh_token = jwt_tokens["refresh_token"]
                redis_.delete(f"{email}_code")
                return Response(
                    data={"access_token": access_token, "refresh_token": refresh_token},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={
                        "Error": "An error while obtaining tokens occurred",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            user_serializer = UserRegisterSerializer(data={"email": email})
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            email = user_serializer.data.get("email")

            response = requests.post(
                url="https://odd-verve-backend.onrender.com/token/",
                json={
                    "email": email,
                },
            )
            if response.status_code == 200:
                jwt_tokens = response.json()
                access_token = jwt_tokens["access_token"]
                refresh_token = jwt_tokens["refresh_token"]
                redis_.delete(f"{email}_code")
                return Response(
                    data={"access_token": access_token, "refresh_token": refresh_token},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={
                        "Error": "An error while obtaining tokens occurred",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
