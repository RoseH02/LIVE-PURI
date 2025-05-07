
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('vitamins/', views.vitamins, name='vitamins'),
    path('protein/', views.protein, name='protein'),
    path('boutique/meal-substitutes/', views.meal_substitutes, name='meal_substitutes'),
    path('boutique/collagen/', views.collagen, name='collagen'),
    path('boutique/accessories/', views.accessories, name='accessories'),
    path('recipes/', views.recipes, name='recipes'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/', views.cart_detail, name='cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Ensure this line is present
    path('contact/', views.contact, name='contact'),
    path('affilie/', views.affilie, name='affilie'),
    path('livraison/', views.livraison, name='livraison'),








]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


