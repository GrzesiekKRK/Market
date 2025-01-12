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
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:

                login(request, user)
                return redirect('products')
        return render(request, 'users/login.html', {'form': form})

    def get_success_url(self) -> HttpResponse:
        user = CustomUser.objects.get(id=self.request.user.id)

        return render(self.request, 'users/update.html', {'user': user})

    def form_invalid(self, form: LoginForm) -> TemplateResponse:
        # print(form.errors)
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class UserSignUpView(CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('user-login')
    form_class = RegisterUserForm
    success_message = "Your profile was created successfully"

    def form_invalid(self, form):
        # print(form.errors)
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update.html'
    form_class = UpdateUserForm

    def get_object(self, queryset: Optional[QuerySet[CustomUser]] = None) -> CustomUser:
        user = CustomUser.objects.get(id=self.request.user.id)
        return user

    def get_success_url(self) -> HttpResponse:
        user = CustomUser.objects.get(id=self.request.user.id)
        return render(self.request, 'users/update.html', {'user': user})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse | HttpResponseRedirect:
        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect('user-profile')
        else:
            form = form = UpdateUserForm()
        return render(request, 'users/update.html', {'form': form})

    def form_invalid(self, form: UpdateUserForm) -> TemplateResponse:
        messages.error(self.request, 'Invalid change')
        return self.render_to_response(self.get_context_data(form=form))

#TODO get_object
class UserDeleteView(DeleteView, LoginRequiredMixin):
    model = CustomUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user-login')
