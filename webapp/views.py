from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from webapp.models import Product, Review
from webapp.forms import ProductForm, ReviewForm, ReviewModeratorForm


class ProductListView(ListView):
    model = Product
    template_name = "webapp/product_list.html"
    context_object_name = "products"
    paginate_by = 12


class ProductDetailView(DetailView):
    model = Product
    template_name = "webapp/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_staff:
            reviews = self.object.review_set.all()
        else:
            if user.is_authenticated:
                reviews = self.object.review_set.filter(
                    Q(is_moderated=True) | Q(author=user)
                )
            else:
                reviews = self.object.review_set.filter(is_moderated=True)

            context["reviews"] = reviews
            return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "webapp/product_form.html"
    success_url = reverse_lazy("webapp:product_list")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "webapp/product_form.html"
    success_url = reverse_lazy("webapp:product_list")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "webapp/product_confirm_delete.html"
    success_url = reverse_lazy("webapp:product_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.image:
            obj.image.delete(save=False)
        return super().delete(request, *args, **kwargs)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "webapp/review_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:product_detail", kwargs={"pk": self.kwargs["pk"]})


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = "webapp/review_form.html"

    def get_form_class(self):
        if self.request.user.is_staff:
            return ReviewModeratorForm
        return ReviewForm

    def form_valid(self, form):
        review = form.instance

        if not self.request.user.is_staff:
            if review.is_moderated:
                review.is_moderated = False

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:product_detail", kwargs={"pk": self.object.product.pk})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "webapp/review_confirm_delete.html"

    def get_success_url(self):
        return reverse("webapp:product_detail", kwargs={"pk": self.object.product.pk})
