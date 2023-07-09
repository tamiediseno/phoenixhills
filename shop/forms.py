from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from .models import Product, Category, Order, ProductImage

class RegistrationForm(UserCreationForm):
    pass

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'on_promotion', 'flagship']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']

ProductImageFormSet = modelformset_factory(ProductImage, fields=('image', 'is_main'), extra=2, max_num=2)

class ProductFormUpdate(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'on_promotion', 'flagship']

class ProductImageFormUpdate(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']

# Remove this line
# ProductImageFormSet = formset_factory(ProductImageForm, extra=2, max_num=2)

class CategoryForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Category
        fields = ['name', 'image']
