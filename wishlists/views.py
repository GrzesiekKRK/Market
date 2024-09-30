from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from django.views.generic import TemplateView
from django.shortcuts import render, redirect


from .models import Wishlist

from products.models import Product
from icecream import ic


class MyWishlistView(TemplateView):
    template_name = 'wishlist/wishlist.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        wishlist = Wishlist.objects.get_or_create(user=self.request.user)

        context['wishlist'] = wishlist[0]
        context['products'] = wishlist[0].product.all()

        return context

    @staticmethod
    def add_wish(request: HttpRequest, pk: int) -> HttpResponse:
        wishlist = Wishlist.objects.get_or_create(user=request.user)
        wishlist[0].save()
        product = Product.objects.get(id=pk)

        if product:

            wishlist[0].product.add(product)
            products = wishlist[0].product.all()

        else:
            products = wishlist[0].product.all()
        return render(request, 'wishlist/wishlist.html', {'products': products})

    @staticmethod
    def remove_from_wishlist(request: HttpRequest, pk: int) -> HttpResponse:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.save()
        product = Product.objects.get(id=pk)

        if product:
            wishlist.product.remove(product)
            products = wishlist.product.all()
            return render(request, 'wishlist/wishlist.html', {'products': products})

        else:
            products = wishlist.product.all()
        return render(request, 'wishlist/wishlist.html', {'products': products})


