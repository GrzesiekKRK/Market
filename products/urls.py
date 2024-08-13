from django.urls import path
from .views import ProductListView, CategoryView, ProductDetailView, CreateProduct, ProductDeleteView, ProductUpdateView
urlpatterns = [
    path('', ProductListView.as_view(), name='market-products'),
    path('category/<int:pk>/', CategoryView.as_view(), name='market-category-products'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='market-product-detail'),
    path('add_product/', CreateProduct.product_upload, name='market-vendor-add-product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    ]
