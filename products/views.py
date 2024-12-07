from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from django.views.generic import TemplateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render

from products.models import Category, Product
from .models import ProductImage
from .forms import AddProductForm, ImageForm

from inventories.models import Inventory
from wishlists.models import Wishlist
from notifications.models import Notification
from users.models import CustomUser
from icecream import ic


class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'market/index.html'


class ProductListTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'products/products.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str: Any]:
        deals = Product.objects.filter(is_sale=True)
        products = Product.objects.all()
        categories = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['products'] = products
        context['categories'] = categories
        context['deals'] = deals
        return context


class ProductDetailTemplateView(LoginRequiredMixin, TemplateView):
    model = Product
    template_name = 'products/product-detail.html'

    def get_context_data(self, **kwargs) -> dict[str: Any]:
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=context['pk'])
        context['product'] = product
        context['image'] = ProductImage.objects.filter(product=product.id)
        context['miniature'] = ProductImage.objects.filter(product=product.id)[0]
        return context


class CategoryTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'products/category.html'

    def get_context_data(self, **kwargs) -> dict[str: Any]:
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=context['pk'])
        context['category'] = category
        context['categories'] = Category.objects.exclude(id=context['pk'])
        context['products'] = Product.objects.filter(category=category)
        return context


class CreateProduct(LoginRequiredMixin):
    @staticmethod
    def product_upload(request: HttpRequest) -> HttpResponse:
        image_form = ImageForm()
        product_form = AddProductForm()
        if request.method == 'POST':
            product_form = AddProductForm(request.POST)

            images = request.FILES.getlist('image')
            miniature = request.FILES.getlist('miniature')
            if product_form.is_valid():
                user = request.user
                product = product_form.save()
                inventory = Inventory.objects.get_or_create(vendor=user)
                inventory[0].save()
                inventory[0].product.add(product)

                for image in images:
                    image_ins = ProductImage(image=image, product=product)
                    image_ins.save()

                miniature = miniature[0]
                image_ins = ProductImage(image=miniature, product=product, miniature=True)
                image_ins.save()

                return render(request, 'products/product-detail.html', {'product': product})
        context = {'form': image_form, 'product_form': product_form}
        return render(request, "products/add_product.html", context)


class ProductUpdateView(UpdateView):
    template_name = 'products/update.html'
    form_class = AddProductForm
    model = Product

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        product = self.get_object()
        product_form = AddProductForm(instance=product)

        return render(request, 'products/update.html', {'product_form': product_form, 'product': product})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        product = self.get_object()
        product_form = AddProductForm(request.POST, instance=product)

        if product_form.is_valid():
            product_form.save()
            if product.is_sale:
                wishlists_with_product_on_sale = Wishlist.objects.filter(product=product)
                for wishlist_owner in wishlists_with_product_on_sale:
                    title = f"Special Offer: {product.name}"
                    body = f"<a href =\"http://127.0.0.1:8000/products/detail/{product.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>{product.name}</a>"
                    user = CustomUser.objects.get(id=wishlist_owner.user.id)
                    notification = Notification(user=user, title=title, body=body)
                    notification.save()

            return render(request, 'products/product-detail.html', {'product': product, })
        elif not product_form.is_valid():
            return render(request, 'products/update.html', {'product_form': product_form, 'product': product})

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid change')
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('products')


