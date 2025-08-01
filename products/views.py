from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, TemplateView, UpdateView
from django.core.exceptions import ValidationError

from inventories.models import Inventory
from notifications.models import Notification
from products.filters import ProductFilter
from products.models import Category, Product, ProductDimension
from products.permissions import product_owner_required
from wishlists.models import Wishlist


from .forms import (
    AddProductForm,
    ImageForm,
    ProductDimensionForm,
    UpdateProductDimensionForm,
)
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
        product_filter = ProductFilter(self.request.GET or None, queryset=products)
        filtered_products = product_filter.qs

        paginator = Paginator(filtered_products, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number) if page_number else 1
        except (TypeError, ValueError):
            page_number = 1

        page_obj = paginator.get_page(page_number)
        categories = Category.objects.all()

        context = super().get_context_data(**kwargs)

        context["products"] = page_obj  # paginated filtered products
        context["categories"] = categories
        context["deals"] = deals
        context["filter"] = product_filter  # pass the filter object

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
        context["images"] = ProductImage.objects.filter(product=product.id).order_by('-miniature', 'created_at')

        # Bezpieczne pobieranie miniaturki
        miniature_image = ProductImage.objects.filter(product=product.id, miniature=True).first()
        if not miniature_image:
            miniature_image = ProductImage.objects.filter(product=product.id).first()
        context["miniature"] = miniature_image

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
        Updated to work with S3 storage and better error handling.

        Args:
            request (HttpRequest): The HTTP request containing product data.

        Returns:
            HttpResponse: The HTTP response to render the product detail page or the
                           product creation form.
        """
        image_form = ImageForm()
        product_dimension_form = ProductDimensionForm()
        product_form = AddProductForm()

        if request.method == "POST":
            product_form = AddProductForm(request.POST)
            product_dimension_form = ProductDimensionForm(request.POST)

            images = request.FILES.getlist("image")
            miniature = request.FILES.getlist("miniature")

            if product_form.is_valid() and product_dimension_form.is_valid():
                try:
                    user = request.user
                    product = product_form.save()
                    inventory = Inventory.objects.get_or_create(vendor=user)
                    inventory[0].save()
                    inventory[0].products.add(product)
                    ProductDimension.creation(product, product_dimension_form)

                    # Upload regular images
                    uploaded_images = 0
                    for image in images:
                        try:
                            image_ins = ProductImage(image=image, product=product)
                            image_ins.save()
                            uploaded_images += 1
                        except ValidationError as e:
                            messages.error(request, f"Error uploading image {image.name}: {', '.join(e.messages)}")
                        except Exception as e:
                            messages.error(request, f"Error uploading image {image.name}: {str(e)}")

                    # Upload miniature image
                    if miniature:
                        try:
                            miniature_file = miniature[0]
                            image_ins = ProductImage(
                                image=miniature_file, product=product, miniature=True
                            )
                            image_ins.save()
                            uploaded_images += 1
                        except ValidationError as e:
                            messages.error(request, f"Error uploading miniature: {', '.join(e.messages)}")
                        except Exception as e:
                            messages.error(request, f"Error uploading miniature: {str(e)}")
                    elif uploaded_images > 0:
                        # If no miniature specified, make first image the miniature
                        first_image = ProductImage.objects.filter(product=product).first()
                        if first_image:
                            first_image.miniature = True
                            first_image.save()

                    if uploaded_images > 0:
                        messages.success(request,
                                         f"Product created successfully with {uploaded_images} images uploaded to S3!")
                    else:
                        messages.warning(request, "Product created but no images were uploaded.")

                    return render(
                        request, "products/product-detail.html", {"product": product}
                    )

                except Exception as e:
                    messages.error(request, f"Error creating product: {str(e)}")

        context = {
            "form": image_form,
            "product_form": product_form,
            "product_dimension_form": product_dimension_form,
        }
        return render(request, "products/add_product.html", context)


def upload_product_images(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Dedicated view for uploading additional images to existing product.

    Args:
        request (HttpRequest): The HTTP request containing image data.
        product_id (int): ID of the product to add images to.

    Returns:
        HttpResponse: JSON response for AJAX or redirect for regular form.
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if user owns the product (add your permission logic here)
    # if not product_owner_check(request.user, product):
    #     messages.error(request, "You don't have permission to upload images for this product.")
    #     return redirect('product_detail', pk=product_id)

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        make_miniature = request.POST.get('make_miniature', False)

        if not images:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'No images selected'})
            messages.error(request, 'No images selected.')
            return redirect('product_detail', pk=product_id)

        uploaded_count = 0
        errors = []

        for i, image in enumerate(images):
            try:
                is_miniature = False
                if make_miniature and i == 0:

                    ProductImage.objects.filter(product=product, miniature=True).update(miniature=False)
                    is_miniature = True
                elif not ProductImage.objects.filter(product=product, miniature=True).exists() and i == 0:
                    is_miniature = True

                product_image = ProductImage(
                    product=product,
                    image=image,
                    miniature=is_miniature
                )
                product_image.save()
                uploaded_count += 1

            except ValidationError as e:
                errors.append(f'{image.name}: {", ".join(e.messages)}')
            except Exception as e:
                errors.append(f'{image.name}: {str(e)}')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': uploaded_count > 0,
                'uploaded_count': uploaded_count,
                'errors': errors,
                'message': f'Successfully uploaded {uploaded_count} images to S3' if uploaded_count > 0 else 'No images uploaded'
            })

        if uploaded_count > 0:
            messages.success(request, f'Successfully uploaded {uploaded_count} images to S3!')

        for error in errors:
            messages.error(request, f'Upload error: {error}')

        return redirect('product_detail', pk=product_id)

    return render(request, 'products/upload_images.html', {
        'product': product,
        'existing_images': ProductImage.objects.filter(product=product).order_by('-miniature', 'created_at')
    })


def delete_product_image(request: HttpRequest, image_id: int) -> HttpResponse:
    """
    Delete a specific product image (removes from S3 as well).

    Args:
        request (HttpRequest): The HTTP request.
        image_id (int): ID of the image to delete.

    Returns:
        HttpResponse: JSON response for AJAX or redirect for regular request.
    """
    image = get_object_or_404(ProductImage, id=image_id)
    product = image.product

    # Check permissions here
    # if not product_owner_check(request.user, product):
    #     return JsonResponse({'success': False, 'error': 'Permission denied'})

    try:
        image.delete()  # This will also delete from S3 due to our custom delete method

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Image deleted successfully from S3'
            })

        messages.success(request, 'Image deleted successfully from S3!')
        return redirect('product_detail', pk=product.id)

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': f'Error deleting image: {str(e)}'
            })

        messages.error(request, f'Error deleting image: {str(e)}')
        return redirect('product_detail', pk=product.id)


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
        product_dimension = ProductDimension.objects.get(product=product)
        product_dimension_form = UpdateProductDimensionForm(instance=product_dimension)

        # Add existing images to context
        existing_images = ProductImage.objects.filter(product=product).order_by('-miniature', 'created_at')

        return render(
            request,
            "products/update.html",
            {
                "product_form": product_form,
                "product": product,
                "product_dimension_form": product_dimension_form,
                "existing_images": existing_images,
            },
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
        product_dimension = ProductDimension.objects.get(product=product)
        product_dimension_form = UpdateProductDimensionForm(
            request.POST, instance=product_dimension
        )

        if product_form.is_valid() and product_dimension_form.is_valid():
            product_form.save()
            product_dimension_form.save()

            if product.is_sale:
                wishlists_with_product_on_sale = (
                    Wishlist.objects.filter(product=product),
                )
                for wishlist_owner in wishlists_with_product_on_sale:
                    Notification.create_wishlist_notification(wishlist_owner, product)

            messages.success(request, "Product updated successfully!")

        return render(
            request,
            "products/product-detail.html",
            {
                "product": product,
                "images": ProductImage.objects.filter(product=product).order_by('-miniature', 'created_at'),
            },
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

    def delete(self, request, *args, **kwargs):
        """
        Override delete to ensure all associated images are deleted from S3.
        """
        product = self.get_object()

        # Delete all associated images (this will trigger S3 deletion via our custom delete method)
        images = ProductImage.objects.filter(product=product)
        for image in images:
            try:
                image.delete()
            except Exception as e:
                messages.warning(request, f"Error deleting image from S3: {str(e)}")

        messages.success(request, "Product and all associated images deleted successfully from S3!")
        return super().delete(request, *args, **kwargs)

# from typing import Any
#
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.paginator import Paginator
# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.generic import DeleteView, TemplateView, UpdateView
#
# from inventories.models import Inventory
# from notifications.models import Notification
# from products.filters import ProductFilter
# from products.models import Category, Product, ProductDimension
# from products.permissions import product_owner_required
# from wishlists.models import Wishlist
#
# from .forms import (
#     AddProductForm,
#     ImageForm,
#     ProductDimensionForm,
#     UpdateProductDimensionForm,
# )
# from .models import ProductImage
#
#
# class BaseView(LoginRequiredMixin, TemplateView):
#     """
#     Base view for the home page or landing page of the market.
#     """
#
#     template_name = "market/index.html"
#
#
# class ProductListTemplateView(LoginRequiredMixin, TemplateView):
#     """
#     View for displaying the list of products, including products on sale and all categories.
#     """
#
#     template_name = "products/products.html"
#
#     def get_context_data(self, **kwargs) -> dict[str:Any]:
#         """
#         Prepares the context data for the product list page, including all products,
#         categories, and products on sale.
#
#         Args:
#             **kwargs: Arbitrary keyword arguments passed from the template context.
#
#         Returns:
#             dict[str: Any]: Context data to be rendered in the template.
#         """
#         deals = Product.objects.filter(is_sale=True)
#         products = (
#             Product.objects.select_related("category").prefetch_related("image").all()
#         )
#         product_filter = ProductFilter(self.request.GET or None, queryset=products)
#         filtered_products = product_filter.qs
#
#         paginator = Paginator(filtered_products, 12)
#         page_number = self.request.GET.get("page")
#         try:
#             page_number = int(page_number) if page_number else 1
#         except (TypeError, ValueError):
#             page_number = 1
#
#         page_obj = paginator.get_page(page_number)
#         categories = Category.objects.all()
#
#         context = super().get_context_data(**kwargs)
#
#         context["products"] = page_obj  # paginated filtered products
#         context["categories"] = categories
#         context["deals"] = deals
#         context["filter"] = product_filter  # pass the filter object
#
#         return context
#
#
# class ProductDetailTemplateView(LoginRequiredMixin, TemplateView):
#     """
#     View for displaying detailed information about a specific product.
#     """
#
#     model = Product
#     template_name = "products/product-detail.html"
#
#     def get_context_data(self, **kwargs) -> dict[str:Any]:
#         """
#         Prepares the context data for the product detail page, including the product
#         information and associated images.
#
#         Args:
#             **kwargs: Arbitrary keyword arguments passed from the template context.
#
#         Returns:
#             dict[str: Any]: Context data to be rendered in the template.
#         """
#         context = super().get_context_data(**kwargs)
#         product = (
#             Product.objects.select_related("category")
#             .prefetch_related("image")
#             .get(id=context["pk"])
#         )
#         context["product"] = product
#         context["image"] = ProductImage.objects.filter(product=product.id)
#         context["miniature"] = ProductImage.objects.filter(product=product.id)[0]
#         return context
#
#
# class CategoryTemplateView(LoginRequiredMixin, TemplateView):
#     """
#     View for displaying a specific category's products and other categories.
#     """
#
#     template_name = "products/category.html"
#
#     def get_context_data(self, **kwargs) -> dict[str:Any]:
#         """
#         Prepares the context data for the category page, including the selected category
#         and the products associated with it.
#
#         Args:
#             **kwargs: Arbitrary keyword arguments passed from the template context.
#
#         Returns:
#             dict[str: Any]: Context data to be rendered in the template.
#         """
#         context = super().get_context_data(**kwargs)
#         category = Category.objects.get(id=context["pk"])
#         products = (
#             Product.objects.select_related("category")
#             .prefetch_related("image")
#             .filter(category=category)
#         )
#         paginator = Paginator(products, 12)
#         page_number = self.request.GET.get("page")
#         try:
#             page_number = int(page_number)
#         except (TypeError, ValueError):
#             page_number = 1
#         page_obj = paginator.get_page(page_number)
#         context["category"] = category
#         context["categories"] = Category.objects.exclude(id=context["pk"])
#         context["products"] = page_obj
#         return context
#
#
# class CreateProduct(LoginRequiredMixin):
#     """
#     View for handling the creation of a new product. This includes uploading images
#     and adding product details to the database.
#     """
#
#     @staticmethod
#     def product_upload(request: HttpRequest) -> HttpResponse:
#         """
#         Handles the POST request to create a new product and upload associated images.
#
#         Args:
#             request (HttpRequest): The HTTP request containing product data.
#
#         Returns:
#             HttpResponse: The HTTP response to render the product detail page or the
#                            product creation form.
#         """
#         image_form = ImageForm()
#         product_dimension_form = ProductDimensionForm()
#         product_form = AddProductForm()
#
#         if request.method == "POST":
#             product_form = AddProductForm(request.POST)
#             product_dimension_form = ProductDimensionForm(request.POST)
#
#             images = request.FILES.getlist("image")
#             miniature = request.FILES.getlist("miniature")
#             if product_form.is_valid() and product_dimension_form.is_valid():
#                 user = request.user
#                 product = product_form.save()
#                 inventory = Inventory.objects.get_or_create(vendor=user)
#                 inventory[0].save()
#                 inventory[0].products.add(product)
#                 ProductDimension.creation(product, product_dimension_form)
#                 for image in images:
#                     image_ins = ProductImage(image=image, product=product)
#                     image_ins.save()
#
#                 miniature = miniature[0]
#                 image_ins = ProductImage(
#                     image=miniature, product=product, miniature=True
#                 )
#                 image_ins.save()
#
#                 return render(
#                     request, "products/product-detail.html", {"product": product}
#                 )
#         context = {
#             "form": image_form,
#             "product_form": product_form,
#             "product_dimension_form": product_dimension_form,
#         }
#         return render(request, "products/add_product.html", context)
#
#
# @method_decorator(product_owner_required(), name="dispatch")
# class ProductUpdateView(LoginRequiredMixin, UpdateView):
#     """
#     View for updating an existing product. This view allows the vendor to update
#     product details, such as price, description, and sale status.
#     """
#
#     template_name = "products/update.html"
#     form_class = AddProductForm
#     model = Product
#
#     def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
#         """
#         Handles the GET request to display the product update form.
#
#         Args:
#             request (HttpRequest): The HTTP request.
#             *args: Variable length argument list.
#             **kwargs: Arbitrary keyword arguments.
#
#         Returns:
#             HttpResponse: The response to render the update form with the current product data.
#         """
#         product = self.get_object()
#         product_form = AddProductForm(instance=product)
#         product_dimension = ProductDimension.objects.get(product=product)
#         product_dimension_form = UpdateProductDimensionForm(instance=product_dimension)
#         return render(
#             request,
#             "products/update.html",
#             {
#                 "product_form": product_form,
#                 "product": product,
#                 "product_dimension_form": product_dimension_form,
#             },
#         )
#
#     def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
#         """
#         Handles the POST request to update the product with new data.
#
#         Args:
#             request (HttpRequest): The HTTP request containing the updated product data.
#
#         Returns:
#             HttpResponse: The response to render the updated product detail page or re-display
#                            the form with validation errors.
#         """
#         product = self.get_object()
#         product_form = AddProductForm(request.POST, instance=product)
#         product_dimension = ProductDimension.objects.get(product=product)
#         product_dimension_form = UpdateProductDimensionForm(
#             request.POST, instance=product_dimension
#         )
#
#         if product_form.is_valid() and product_dimension_form.is_valid():
#             product_form.save()
#             product_dimension_form.save()
#
#             if product.is_sale:
#                 wishlists_with_product_on_sale = (
#                     Wishlist.objects.filter(product=product),
#                 )
#                 for wishlist_owner in wishlists_with_product_on_sale:
#                     Notification.create_wishlist_notification(wishlist_owner, product)
#         return render(
#             request,
#             "products/product-detail.html",
#             {
#                 "product": product,
#             },
#         )
#
#     def form_invalid(self, form) -> str:
#         """
#         Handles invalid form submission by showing an error message.
#
#         Args:
#             form (Form): The form that was submitted.
#
#         Returns:
#             str: The response to render the form with error messages.
#         """
#         messages.error(self.request, "Invalid change")
#         return self.render_to_response(self.get_context_data(form=form))
#
#
# @method_decorator(product_owner_required(), name="dispatch")
# class ProductDeleteView(LoginRequiredMixin, DeleteView):
#     model = Product
#     template_name = "products/delete.html"
#     success_url = reverse_lazy("products")
