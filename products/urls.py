from django.urls import path
from .views import ProductListTemplateView, CategoryTemplateView, ProductDetailTemplateView, CreateProduct, ProductDeleteView, ProductUpdateView
urlpatterns = [
    path('', ProductListTemplateView.as_view(), name='products'),
    path('category/<int:pk>/', CategoryTemplateView.as_view(), name='category-products'),
    path('detail/<int:pk>/', ProductDetailTemplateView.as_view(), name='product-detail'),
    path('add_product/', CreateProduct.product_upload, name='vendor-add-product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    ]
