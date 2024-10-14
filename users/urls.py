from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import UserSignUpView, UserUpdateView, UserLoginView, UserDeleteView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(next_page="user-login"), name='user-logout'),
    path('register/', UserSignUpView.as_view(), name='user-register'),
    path('profile/', UserUpdateView.as_view(), name='user-profile'),
    path('<int:pk>//delete/', UserDeleteView.as_view(), name='user-delete'),
    ]
