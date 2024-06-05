from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterUserForm, LoginForm
from django.contrib import messages


def register(request):# TODO Class Based View.
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account's been created for {username}.")
            return redirect('market-home')
    else:
        form = RegisterUserForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('market-home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

