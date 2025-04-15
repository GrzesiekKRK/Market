from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, View

from products.models import Product

from .models import Wishlist


class WishListTemplateView(LoginRequiredMixin, TemplateView):
    """
    Displays the user's wishlist with a list of products.
    """

    template_name = "wishlist/wishlist.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Retrieves the user's wishlist and associated products.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the context data.

        Returns:
            dict[str, Any]: A dictionary containing the wishlist and its products.
        """
        context = super().get_context_data(**kwargs)
        wishlist, _ = Wishlist.objects.prefetch_related("products").get_or_create(
            user=self.request.user
        )
        products = (
            wishlist.products.select_related("category").prefetch_related("image").all()
        )
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        page_obj = paginator.get_page(page_number)

        context["wishlist"] = wishlist
        context["products"] = page_obj

        return context


class WishlistAddProductView(LoginRequiredMixin, View):
    """
    Adds a product to the user's wishlist.
    """

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Adds the specified product to the user's wishlist.

        Args:
            request (HttpRequest): The HTTP request object containing the user's data.
            pk (int): The ID of the product to add to the wishlist.

        Returns:
            HttpResponse: A response containing the updated list of products in the wishlist.
        """
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        if not created:
            wishlist.save()

        product = get_object_or_404(Product, id=pk)

        wishlist.products.add(product)
        products = (
            wishlist.products.select_related("category").prefetch_related("image").all()
        )
        return render(request, "wishlist/wishlist.html", {"products": products})


class WishlistRemoveProductView(View, LoginRequiredMixin):
    """
    Removes a product from the user's wishlist.
    """

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Removes the specified product from the user's wishlist.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The ID of the product to remove from the wishlist.

        Returns:
            HttpResponse: A response with the updated wishlist products.
        """

        product = get_object_or_404(Product, id=pk)

        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            return render(request, "wishlist/wishlist.html", {"products": []})

        wishlist.products.remove(product)

        wishlist.refresh_from_db()

        return render(request, "wishlist/wishlist.html", {"products": wishlist})
