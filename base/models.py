from django.db import models
from django import forms
from ckeditor.fields import RichTextField

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_best_seller = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/')
    ingredients = models.CharField(max_length=500, blank=True)
    valeur_nutritive  = models.CharField(max_length=500, blank=True)
    reviews = models.CharField(max_length=500, blank=True)
    utilisation = models.CharField(max_length=500, blank=True)

    CATEGORY_CHOICES = [
        ('vitamins', 'Vitamins'),
        ('protein', 'Protein'),
        ('meal_subs', 'Meal Substitutes'),
        ('collagen', 'Collagen'),
        ('accessories', 'Accessories'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    ingredients = models.TextField()
    preparation_steps = RichTextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
