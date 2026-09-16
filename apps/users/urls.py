from django.urls import path

from apps.users.views import UserRegisterView, UserListView, UserDetailView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("", UserListView.as_view(), name="users")
]

app_name = "users"
