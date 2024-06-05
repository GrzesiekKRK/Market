from django.shortcuts import render, redirect, get_object_or_404
from products.models import Department, Category, Product
from django.contrib import messages


def home(request):
    products = Product.objects.all()
    return render(request, 'market/index.html', {'products': products})


def shop(request):
    products = Product.objects.all()
    departments = Department.objects.all()
    categories = Category.objects.all()
    return render(request, "market/shop.html", {'products': products,
                                                                    'departments': departments,
                                                                    'categories': categories})


def category_products(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category=category)
    return render(request, "market/category-products.html", {'category': category,
                                                                               'products': products})


def checkout(request):
    return render(request, "market/checkout.html")


def testimonial(request):
    return render(request, "market/testimonial.html")


def page_not_found(request):
    return render(request, "market/404.html")


def contact(request):
    return render(request, "market/contact.html")


