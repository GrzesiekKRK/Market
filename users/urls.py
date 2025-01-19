from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserDeleteView, UserLoginView, UserSignUpView, UserUpdateView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(next_page="user-login"), name="user-logout"),
    path("register/", UserSignUpView.as_view(), name="user-register"),
    path("profile/", UserUpdateView.as_view(), name="user-profile"),
    path("<int:pk>//delete/", UserDeleteView.as_view(), name="user-delete"),
]
