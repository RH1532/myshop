from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='subcategory_images/')
    parent_category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_small = models.ImageField(upload_to='product_images/small/', null=True, blank=True, default='default_image.jpg')
    image_medium = models.ImageField(upload_to='product_images/medium/', null=True, blank=True, default='default_image.jpg')
    image_large = models.ImageField(upload_to='product_images/large/', null=True, blank=True, default='default_image.jpg')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
