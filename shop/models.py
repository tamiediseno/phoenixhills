from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add any additional fields to store customer data

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/')


    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    customers = models.ManyToManyField(Customer)
    on_promotion = models.BooleanField(default=False)
    flagship = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    def main_image(self):
        return self.images.filter(is_main=True).first()

    def short_description(self, max_length=100):
        if len(self.description) > max_length:
            return self.description[:max_length] + '...'
        else:
            return self.description


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)

    def image_tag(self):
        return format_html('<img src="{}" width="150" height="150" />', self.image.url)

    image_tag.short_description = 'Image'  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # add any additional fields to store order data

    def __str__(self):
        return f'Order {self.id}'

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    # add any additional fields to store payment data

    def __str__(self):
        return f'Payment for Order {self.order.id}'
