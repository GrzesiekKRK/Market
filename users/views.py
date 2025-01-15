from typing import Optional
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib import messages
from .forms import RegisterUserForm, LoginForm, UpdateUserForm
from .models import CustomUser


class UserLoginView(LoginView):
    """
        Handles user login functionality. If the user is already authenticated, they are redirected
        to the products page. If login fails, an error message is shown.
    """
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
            Handles the POST request for user login. It validates the login form, authenticates
            the user, and redirects to the products page if successful.

            Args:
                request (HttpRequest): The HTTP request object.
                *args, **kwargs: Additional arguments for the method.

            Returns:
                HttpResponse: The response after processing the login request.
        """
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:

                login(request, user)
                return redirect("products")
        return render(request, "users/login.html", {"form": form})

    def get_success_url(self) -> HttpResponse:
        """
            Returns the URL to redirect the user to after a successful login.

            Returns:
                HttpResponse: The response with the success URL.
        """
        user = CustomUser.objects.get(id=self.request.user.id)

        return render(self.request, "users/update.html", {"user": user})

    def form_invalid(self, form: LoginForm) -> TemplateResponse:
        """
                Handles the case where the login form is invalid. Displays an error message.

                Args:
                    form (LoginForm): The invalid form that was submitted.

                Returns:
                    TemplateResponse: The rendered template with the form and error messages.
        """
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class UserSignUpView(CreateView):
    """
        Handles the user signup functionality. After successfully registering, the user is redirected
        to the login page.
    """
    template_name = "users/register.html"
    success_url = reverse_lazy("user-login")
    form_class = RegisterUserForm
    success_message = "Your profile was created successfully"

    def form_invalid(self, form) -> str:
        """
                Handles the case where the signup form is invalid.

                Args:
                    form (form): The invalid form that was submitted.

                Returns:
                    str: The template rendered with the invalid form.
        """
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
        Handles updating the user's profile information. Only authenticated users can update their
        profile.
    """
    template_name = "users/update.html"
    form_class = UpdateUserForm

    def get_object(self, queryset: Optional[QuerySet[CustomUser]] = None) -> CustomUser:
        """
                Retrieves the current user's profile to be updated.

                Args:
                    queryset (Optional[QuerySet[CustomUser]]): The queryset used for filtering users.

                Returns:
                    CustomUser: The current user's profile.
        """
        user = CustomUser.objects.get(id=self.request.user.id)
        return user

    def get_success_url(self) -> HttpResponse:
        """
                Returns the URL to redirect to after a successful profile update.

                Returns:
                    HttpResponse: The response with the success URL.
        """
        user = CustomUser.objects.get(id=self.request.user.id)
        return render(self.request, "users/update.html", {"user": user})

    def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponse | HttpResponseRedirect:
        """
                Handles the POST request for updating the user's profile. If the form is valid,
                it saves the changes and redirects the user to their updated profile page.

                Args:
                    request (HttpRequest): The HTTP request object.
                    *args, **kwargs: Additional arguments for the method.

                Returns:
                    HttpResponse | HttpResponseRedirect: The response after processing the update.
        """
        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile is updated successfully")
                return redirect("user-profile")
        else:
            form = form = UpdateUserForm()
        return render(request, "users/update.html", {"form": form})

    def form_invalid(self, form: UpdateUserForm) -> TemplateResponse:
        """
                Handles the case where the update form is invalid. Displays an error message.

                Args:
                    form (UpdateUserForm): The invalid form that was submitted.

                Returns:
                    TemplateResponse: The rendered template with the form and error messages.
        """
        messages.error(self.request, "Invalid change")
        return self.render_to_response(self.get_context_data(form=form))


class UserDeleteView(DeleteView, LoginRequiredMixin):
    """
        Handles user deletion. The user can delete their account, after which they are redirected
        to the login page.
    """
    model = CustomUser
    template_name = "users/delete.html"
    success_url = reverse_lazy("user-login")
