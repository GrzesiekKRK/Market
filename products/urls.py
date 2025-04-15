from django.urls import path

from .views import (
    CategoryTemplateView,
    CreateProduct,
    ProductDeleteView,
    ProductDetailTemplateView,
    ProductListTemplateView,
    ProductUpdateView,
)

urlpatterns = [
    path("products/", ProductListTemplateView.as_view(), name="products"),
    path(
        "categories/<int:pk>/", CategoryTemplateView.as_view(), name="category-products"
    ),
    path(
        "products/<int:pk>/detail/",
        ProductDetailTemplateView.as_view(),
        name="product-detail",
    ),
    path("add-product/", CreateProduct.product_upload, name="vendor-add-product"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"
    ),
]
