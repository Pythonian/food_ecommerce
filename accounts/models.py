# from django.core.validators import MinLengthValidator, MaxLengthValidator
# from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class Vendor(models.Model):
    """ Vendor model for storing vendor information. """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='vendor')
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=600)
    about = models.TextField()
    image = models.ImageField(upload_to='vendor/images')
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return self.company_name


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='customer')
    phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    image = models.ImageField(
        upload_to='customer/images', blank=True, null=True)
    address = models.CharField(
        max_length=250, blank=True, null=True)

    @property
    def email(self):
        return f"{self.user.email}"

    def __str__(self):
        return f"{self.user.username} profile"


class LecturerPreference(models.Model):
    lecturer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    preferred_calories = models.IntegerField(blank=True, null=True)
    preferred_protein = models.IntegerField(blank=True, null=True)
    preferred_carbohydrates = models.IntegerField(blank=True, null=True)
    preferred_fats = models.IntegerField(blank=True, null=True)
    preferred_vitamins = models.IntegerField(blank=True, null=True)
    preferred_minerals = models.IntegerField(blank=True, null=True)
    preferred_fiber = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Food preference for #{self.lecturer.user.username}"
