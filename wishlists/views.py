from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from products.models import Product

from .models import Wishlist


class WishListTemplateView(TemplateView, LoginRequiredMixin):
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
        wishlist, create = Wishlist.objects.prefetch_related("products").get_or_create(
            user=self.request.user
        )

        context["wishlist"] = wishlist
        context["products"] = (
            wishlist.products.select_related("category").prefetch_related("image").all()
        )

        return context


class WishlistAddProductView(View, LoginRequiredMixin):
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

        product = Product.objects.get(id=pk)

        if product:

            wishlist.products.add(product)
            products = (
                wishlist.products.select_related("category")
                .prefetch_related("image")
                .all()
            )

        else:
            products = wishlist.products.all()
        return render(request, "wishlist/wishlist.html", {"products": products})


class WishlistRemoveProductView(View, LoginRequiredMixin):
    """
    Removes a product from the user's wishlist.
    """

    def get(self, request, pk) -> None:
        """
        Prevents access via GET method for this view.

        Args:
            request: The HTTP request object.
            pk: The ID of the product to be removed (not used here).

        Raises:
            Http404: The page cannot be accessed via GET method.
        """
        raise Http404("This page cannot be accessed via GET method.")

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Removes the specified product from the user's wishlist.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The ID of the product to remove from the wishlist.

        Returns:
            HttpResponse: A response with the updated wishlist products.
        """
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return HttpResponse(status=404, content="Product not found.")

        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            return render(request, "wishlist/wishlist.html", {"products": []})

        wishlist.products.remove(product)

        products = wishlist.products.all()

        return render(request, "wishlist/wishlist.html", {"products": products})
