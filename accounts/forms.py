from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Customer, Vendor


class VendorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=200)
    about = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=11)
    company_name = forms.CharField(max_length=50)
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
            field.field.help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2',
                  'company_name', 'address', 'phone_number', 'image', 'about']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        user.refresh_from_db()
        user.vendor.about = self.cleaned_data.get('about')
        user.vendor.email = self.cleaned_data.get('email')
        user.vendor.phone_number = self.cleaned_data.get('phone_number')
        user.vendor.company_name = self.cleaned_data.get('company_name')
        user.vendor.image = self.cleaned_data.get('image')
        user.vendor.address = self.cleaned_data.get('address')
        user.save()
        return user


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
            field.field.help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'image']


class VendorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vendor
        fields = ['company_name', 'address', 'image', 'about', 'phone_number']
