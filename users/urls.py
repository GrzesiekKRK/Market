from django.urls import path, include
from django.contrib.auth.views import LogoutView
from users import views as users_views


urlpatterns = [
    path('login/', users_views.user_login, name='user-login'),
    path("logout/", LogoutView.as_view(next_page="user-login"), name='user-logout'),
    path('register/', users_views.register, name='user-register')
    ]
