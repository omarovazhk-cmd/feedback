from django.urls import path
from webapp.views import (ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView,)

app_name = "webapp"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("product/<int:pk>/review/create/", ReviewCreateView.as_view(), name="review_create"),
    path("review/<int:pk>/edit/", ReviewUpdateView.as_view(), name="review_edit"),
    path("review/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review_delete"),
]
