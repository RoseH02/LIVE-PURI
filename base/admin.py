from django.contrib import admin
from .models import Product
from .models import Recipe  # <-- Make sure this import is here
from .forms import RecipeForm  # <-- Your custom form for Recipe



class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_best_seller')
    list_filter = ('category', 'is_best_seller')

admin.site.register(Product, ProductAdmin)

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    list_display = ('title', 'created_at', 'image')
    search_fields = ('title',)
    list_filter = ('created_at',)

admin.site.register(Recipe, RecipeAdmin)
