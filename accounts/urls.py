from django.urls import path
from accounts.views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView, LoginView, LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="profile"),
    path("profile/edit/", UserChangeView.as_view(), name="profile_edit"),
    path("password-change/", UserPasswordChangeView.as_view(), name="password_change"),
]
