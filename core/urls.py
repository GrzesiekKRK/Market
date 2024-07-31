
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkout/', views.checkout, name='market-checkout'),
    path('testimonial/', views.testimonial, name='market-testimonial'),
    path('contact/', views.ConcatView.as_view(), name='market-contact'),
    path('', views.DashboardView.as_view(), name='market-dashboard'),
    path('products/', include('products.urls')),
    path('shop/', include('cart.urls')),
    path('accounts/', include('users.urls')),
    path('inventory/', include('inventories.urls')),
    path('order/', include('orders.urls')),
    path('wishlist/', include('wishlists.urls')),
    path('messages/', include('notifications.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
