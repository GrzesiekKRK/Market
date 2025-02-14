from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, TemplateView, UpdateView

from inventories.models import Inventory
from notifications.models import Notification
from products.models import Category, Product
from products.permissions import product_owner_required
from users.models import CustomUser
from wishlists.models import Wishlist

from .forms import AddProductForm, ImageForm
from .models import ProductImage


class BaseView(LoginRequiredMixin, TemplateView):
    """
    Base view for the home page or landing page of the market.
    """

    template_name = "market/index.html"


class ProductListTemplateView(LoginRequiredMixin, TemplateView):
    """
    View for displaying the list of products, including products on sale and all categories.
    """

    template_name = "products/products.html"

    def dispatch(self, *args, **kwargs) -> dict[str:Any]:
        """
        Handles the HTTP request and prepares the response by dispatching the request
        to the appropriate handler.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict[str: Any]: The result of the super().dispatch call.
        """
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Prepares the context data for the product list page, including all products,
        categories, and products on sale.

        Args:
            **kwargs: Arbitrary keyword arguments passed from the template context.

        Returns:
            dict[str: Any]: Context data to be rendered in the template.
        """
        deals = Product.objects.filter(is_sale=True)
        products = (
            Product.objects.select_related("category").prefetch_related("image").all()
        )
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()

        context = super().get_context_data(**kwargs)

        context["products"] = page_obj
        context["categories"] = categories
        context["deals"] = deals
        return context


class ProductDetailTemplateView(LoginRequiredMixin, TemplateView):
    """
    View for displaying detailed information about a specific product.
    """

    model = Product
    template_name = "products/product-detail.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Prepares the context data for the product detail page, including the product
        information and associated images.

        Args:
            **kwargs: Arbitrary keyword arguments passed from the template context.

        Returns:
            dict[str: Any]: Context data to be rendered in the template.
        """
        context = super().get_context_data(**kwargs)
        product = (
            Product.objects.select_related("category")
            .prefetch_related("image")
            .get(id=context["pk"])
        )
        context["product"] = product
        context["image"] = ProductImage.objects.filter(product=product.id)
        context["miniature"] = ProductImage.objects.filter(product=product.id)[0]
        return context


class CategoryTemplateView(LoginRequiredMixin, TemplateView):
    """
    View for displaying a specific category's products and other categories.
    """

    template_name = "products/category.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Prepares the context data for the category page, including the selected category
        and the products associated with it.

        Args:
            **kwargs: Arbitrary keyword arguments passed from the template context.

        Returns:
            dict[str: Any]: Context data to be rendered in the template.
        """
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=context["pk"])
        products = (
            Product.objects.select_related("category")
            .prefetch_related("image")
            .filter(category=category)
        )
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        page_obj = paginator.get_page(page_number)
        context["category"] = category
        context["categories"] = Category.objects.exclude(id=context["pk"])
        context["products"] = page_obj
        return context


class CreateProduct(LoginRequiredMixin):
    """
    View for handling the creation of a new product. This includes uploading images
    and adding product details to the database.
    """

    @staticmethod
    def product_upload(request: HttpRequest) -> HttpResponse:
        """
        Handles the POST request to create a new product and upload associated images.

        Args:
            request (HttpRequest): The HTTP request containing product data.

        Returns:
            HttpResponse: The HTTP response to render the product detail page or the
                           product creation form.
        """
        image_form = ImageForm()
        product_form = AddProductForm()
        if request.method == "POST":
            product_form = AddProductForm(request.POST)

            images = request.FILES.getlist("image")
            miniature = request.FILES.getlist("miniature")
            if product_form.is_valid():
                user = request.user
                product = product_form.save()
                inventory = Inventory.objects.get_or_create(vendor=user)
                inventory[0].save()
                inventory[0].products.add(product)

                for image in images:
                    image_ins = ProductImage(image=image, product=product)
                    image_ins.save()

                miniature = miniature[0]
                image_ins = ProductImage(
                    image=miniature, product=product, miniature=True
                )
                image_ins.save()

                return render(
                    request, "products/product-detail.html", {"product": product}
                )
        context = {"form": image_form, "product_form": product_form}
        return render(request, "products/add_product.html", context)


@method_decorator(product_owner_required(), name="dispatch")
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing product. This view allows the vendor to update
    product details, such as price, description, and sale status.
    """

    template_name = "products/update.html"
    form_class = AddProductForm
    model = Product

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the GET request to display the product update form.

        Args:
            request (HttpRequest): The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response to render the update form with the current product data.
        """
        product = self.get_object()
        product_form = AddProductForm(instance=product)

        return render(
            request,
            "products/update.html",
            {"product_form": product_form, "product": product},
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request to update the product with new data.

        Args:
            request (HttpRequest): The HTTP request containing the updated product data.

        Returns:
            HttpResponse: The response to render the updated product detail page or re-display
                           the form with validation errors.
        """
        product = self.get_object()
        product_form = AddProductForm(request.POST, instance=product)

        if product_form.is_valid():
            product_form.save()
            if product.is_sale:
                wishlists_with_product_on_sale = Wishlist.objects.filter(
                    product=product
                )
                for wishlist_owner in wishlists_with_product_on_sale:
                    title = f"Special Offer: {product.name}"
                    body = f"<a href =\"http://127.0.0.1:8000/products/detail/{product.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>{product.name}</a>"
                    user = CustomUser.objects.get(id=wishlist_owner.user.id)
                    notification = Notification(user=user, title=title, body=body)
                    notification.save()

            return render(
                request,
                "products/product-detail.html",
                {
                    "product": product,
                },
            )
        elif not product_form.is_valid():
            return render(
                request,
                "products/update.html",
                {"product_form": product_form, "product": product},
            )

    def form_invalid(self, form) -> str:
        """
        Handles invalid form submission by showing an error message.

        Args:
            form (Form): The form that was submitted.

        Returns:
            str: The response to render the form with error messages.
        """
        messages.error(self.request, "Invalid change")
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(product_owner_required(), name="dispatch")
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy("products")
