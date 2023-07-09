from django.contrib import admin
from .models import Customer, Category, Product, Order, Payment,ProductImage

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order']

# Register your models here.
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_tag']
