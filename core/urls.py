from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import ConcatView, DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", DashboardView.as_view(), name="market-dashboard"),
    path("contact/", ConcatView.as_view(), name="market-contact"),
    path("", include("products.urls")),
    path("shop/", include("cart.urls")),
    path("accounts/", include("users.urls")),
    path("inventory/", include("inventories.urls")),
    path("order/", include("orders.urls")),  # orders
    path("wishlist/", include("wishlists.urls")),
    path("notifications/", include("notifications.urls")),
    path("payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
