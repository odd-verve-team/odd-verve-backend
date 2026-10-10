from django.urls import path

from apps.users.views.user_views import (
    send_authentication_code_view,
    authenticate_user_view,
)

urlpatterns = [
    path("authenticate/", authenticate_user_view, name="authenticate"),
    path("code/", send_authentication_code_view, name="send_email_code"),
]

app_name = "users"
