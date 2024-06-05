"""
URL configuration for Market project.

"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='market-home'),
    path('shop/', views.shop, name='market-shop'),
    path('shop/category/<int:pk>', views.category_products, name='market-category-products'),
    path('checkout/', views.checkout, name='market-checkout'),
    path('testimonial/', views.testimonial, name='market-testimonial'),
    path('contact/', views.contact, name='market-contact'),
    path('404/', views.page_not_found, name='market-404'),
    path('shop/', include('cart.urls')),
    path('users/', include('users.urls'))
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
