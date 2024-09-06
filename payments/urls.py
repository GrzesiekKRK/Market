from django.urls import path
from . import views
from . import services


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('stripe-checkout-session/', services.stripe_checkout_session, name='stripe-checkout'),
    path('success/<int:pk>/', views.SuccessView.as_view()),
    path('cancelled/<int:pk>/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
]
