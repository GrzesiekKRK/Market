from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from .views import DashboardView, ConcatView

urlpatterns = [
                path('admin/', admin.site.urls),
                path('', DashboardView.as_view(), name='market-dashboard'),
                path('contact/', ConcatView.as_view(), name='market-contact'),
                path('products/', include('products.urls')),
                path('shop/', include('cart.urls')),
                path('accounts/', include('users.urls')),
                path('inventory/', include('inventories.urls')),
                path('order/', include('orders.urls')),
                path('wishlist/', include('wishlists.urls')),
                path('notifications/', include('notifications.urls')),
                path('payments/', include('payments.urls')),
                ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
