from django.contrib import admin
from .models import Product, ProductVariant
from .models import Recipe  # <-- Make sure this import is here
from .forms import RecipeForm  # <-- Your custom form for Recipe


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_best_seller')
    list_filter = ('category', 'is_best_seller')
    inlines = [ProductVariantInline]

admin.site.register(Product, ProductAdmin)  
admin.site.register(ProductVariant) 

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    list_display = ('title', 'created_at', 'image')
    search_fields = ('title',)
    list_filter = ('created_at',)

admin.site.register(Recipe, RecipeAdmin)
