from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

CATEGORY_CHOICES = [
    ('tech', 'Техника'),
    ('food', 'Еда'),
    ('beauty', 'Красота'),
    ('services', 'Услуги'),
    ('other', 'Другое'),
]


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.review_set.filter(is_moderated=True)
        if not reviews.exists():
            return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    is_moderated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.author} for {self.product}"
