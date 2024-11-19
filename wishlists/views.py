from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from django.views.generic import TemplateView, View, DeleteView
from django.shortcuts import render, redirect


from .models import Wishlist

from products.models import Product
from icecream import ic


class WishListTemplateView(TemplateView):
    template_name = 'wishlist/wishlist.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        wishlist = Wishlist.objects.get_or_create(user=self.request.user)

        context['wishlist'] = wishlist[0]
        context['products'] = wishlist[0].product.all()

        return context


class WishlistAddProductView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        if not created:
            wishlist.save()

        product = Product.objects.get(id=pk)

        if product:

            wishlist.product.add(product)
            products = wishlist.product.all()

        else:
            products = wishlist.product.all()
        return render(request, 'wishlist/wishlist.html', {'products': products})


class WishlistRemoveProductView(View):
    def get(self, request, pk):
        raise Http404("This page cannot be accessed via GET method.")

    #TODO wyjątek
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return HttpResponse(status=404, content="Product not found.")

        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            return render(request, 'wishlist/wishlist.html', {'products': []})

        wishlist.product.remove(product)

        products = wishlist.product.all()

        return render(request, 'wishlist/wishlist.html', {'products': products})



