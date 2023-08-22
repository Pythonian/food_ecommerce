# from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidators
from django.core.files import File
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
# from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from PIL import Image

from accounts.models import User


class Category(models.Model):
    """
    Product category table
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("category name"),
        help_text=_("format: required, max-50"),
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("category safe URL"),
        help_text=_(
            "format: required, letters, numbers, underscore, or hyphens"
        ),
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_("category description"),
        blank=True,
        help_text=_("format: not required, max-1000"),
    )
    icon = models.CharField(max_length=20, help_text="Font awesome icon")

    class Meta:
        ordering = ("name",)
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def get_absolute_url(self):
        return reverse('products:category',
                       kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name=_("products"))
    name = models.CharField(
        unique=True, max_length=255, db_index=True)
    slug = models.SlugField(
        unique=True, max_length=255, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("price"))
    image = models.ImageField(upload_to="images/")
    calories = models.IntegerField(
        help_text="The amount of energy provided by the food.Example: 150 (kcal)")
    protein = models.IntegerField(
        help_text="The amount of protein in the food. Example: 8.5 (g)")
    carbohydrates = models.IntegerField(
        help_text="The total amount of carbohydrates in the food, including sugars, fiber, and starches. Example: 20.3 (g)")
    fats = models.IntegerField(
        help_text="The total amount of fats in the food, including saturated fats and unsaturated fats. Example: 5.2 (g)")
    vitamins = models.IntegerField(
        help_text="The amount of various vitamins present in the food. Example: Vitamin C: 10 mg, Vitamin A: 200 IU")
    minerals = models.IntegerField(
        help_text="The amount of various minerals present in the food. Example: Iron: 2.3 mg, Calcium: 120 mg")
    fiber = models.IntegerField(
        help_text="The amount of dietary fiber in the food. Example: 3.5 (g)")
    delivery_time = models.CharField(
        max_length=100,
        help_text="Time it will take for this food to be delivered.")
    vendor = models.ForeignKey(
        User,
        related_name=_("products"),
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date product last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    objects = models.Manager()
    active = ProductManager()

    class Meta:
        ordering = ("-created",)
        verbose_name = _("product")
        verbose_name_plural = _("products")
        # index_together = (('uuid', 'slug'),)

    def get_absolute_url(self):
        return reverse('products:detail',
                       kwargs={'slug': self.slug})

    def average_review(self):
        reviews = Review.objects.filter(
            product=self, is_visible=True).aggregate(average=Avg('rating'))
        avg = 0.0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = Review.objects.filter(
            product=self, is_visible=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    rating = models.FloatField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent_data = models.CharField(
        max_length=255, blank=True, null=True)
    thumbsup = models.IntegerField(default="0")
    thumbsdown = models.IntegerField(default="0")
    thumbs = models.ManyToManyField(
        User, related_name="thumbs", default=None, blank=True)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.subject


class ReviewVote(models.Model):
    review = models.ForeignKey(
        Review, related_name="reviewid", on_delete=models.CASCADE,
        default=None, blank=True)
    user = models.ForeignKey(
        User, related_name="userid", on_delete=models.CASCADE,
        default=None, blank=True)
    vote = models.BooleanField(default=True)
    