from django.contrib import admin

from .models import Customer, Vendor, User, LecturerPreference


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['company_name']


admin.site.register(User)
admin.site.register(LecturerPreference)