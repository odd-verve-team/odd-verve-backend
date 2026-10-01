from django.urls import path

from apps.users.views import (
    UserListView,
    UserDetailView,
    send_authentication_code_view,
    authenticate_user_view,
)

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("authenticate/", authenticate_user_view, name="authenticate"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("code/", send_authentication_code_view, name="send_email_code"),
]

app_name = "users"
