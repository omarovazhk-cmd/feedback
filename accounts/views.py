from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView, PasswordChangeView as DjangoPasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.shortcuts import redirect

from django.contrib.auth import get_user_model
from .forms import RegisterForm, ProfileEditForm

User = get_user_model()


class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"


class LogoutView(DjangoLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user_object"


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"pk": self.request.user.pk})


class UserPasswordChangeView(DjangoPasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:login")
