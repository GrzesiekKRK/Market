from django.urls import path

from payments import services, views

urlpatterns = [
    path(
        "stripe-checkout-session/",
        services.stripe_checkout_session,
        name="stripe-checkout",
    ),
    path(
        "success/<int:pk>/",
        views.SuccessTemplateView.as_view(),
        name="successful-payment",
    ),
    path(
        "cancel/<int:pk>/",
        views.CancelledTemplateView.as_view(),
        name="cancelled-payment",
    ),
    path("webhook/", views.stripe_webhook),
]
