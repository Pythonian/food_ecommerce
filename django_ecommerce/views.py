from django.shortcuts import render

from products.models import Product, Category
from accounts.models import Vendor, LecturerPreference


def home(request):
    products = None
    recommended_food = None
    preference = None
    vendors = Vendor.objects.all()[:6]
    categories = Category.objects.all()

    # Retrieve the lecturer's preferences
    if request.user.is_authenticated and request.user.is_customer:
        try:
            preference = LecturerPreference.objects.get(
                lecturer=request.user.customer)
            print(preference)
        except LecturerPreference.DoesNotExist:
            # Handle the case where there are no preferences
            preference = None

        # Use the lecturer's preferences to customize the food recommendations
        if preference:
            recommended_food = Product.objects.filter(
                calories__lte=preference.preferred_calories
            )
        else:
            # If there are no preferences, show all available food items
            recommended_food = Product.objects.all()[:12]
    else:
        products = Product.objects.all()[:12]

    template_name = "home.html"
    context = {
        "products": products,
        "vendors": vendors,
        "categories": categories,
        "recommended_food": recommended_food,
        "preference": preference,
    }

    return render(request, template_name, context)
