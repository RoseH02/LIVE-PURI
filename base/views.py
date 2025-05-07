from django.shortcuts import render
from .models import Product 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
import stripe 
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Recipe
from django.core.mail import send_mail






# Create your views here.



def about(request):
    return render(request, 'about.html')

def livraison(request):
    return render(request, 'livraison.html')

def contact(request):
    return render(request, 'contact.html')

def affilie(request):
    return render(request, 'affilie.html')


def vitamins(request):
    products = Product.objects.filter(category='vitamins')
    return render(request, 'vitamins.html', {'products': products})

def protein(request):
    products = Product.objects.filter(category='protein')
    return render(request, 'protein.html', {'products': products})

def meal_substitutes(request):
    products = Product.objects.filter(category='meal_subs')
    return render(request, 'meal_subs.html', {'products': products})


def collagen(request):
    return render(request, 'collagen.html')

def accessories(request):
    return render(request, 'accessories.html')

def home(request):
    latest_recipes = Recipe.objects.order_by('-created_at')[:3]
    best_sellers = Product.objects.filter(is_best_seller=True)
    context = {
        'latest_recipes': latest_recipes,
        'best_sellers': best_sellers
    }
    return render(request, 'home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    request.session.modified = True

    print("Cart after adding:", cart)  # Debug print

    return redirect('cart')  # Make sure this URL name exists


def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    request.session['total_price'] = float(total)  # 🛑 SUPER IMPORTANT 🛑

    return render(request, 'cart_detail.html', {'products': products, 'total': total})




from django.http import JsonResponse

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})  # your cart structure
        subtotals = {}

        # If empty cart requested
        if request.POST.get('empty_cart'):
            request.session['cart'] = {}
            request.session.modified = True
            return JsonResponse({'subtotals': {}, 'total': 0})

        # Update quantities from POST data
        for key, value in request.POST.items():
            if key.startswith('quantities_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity < 0:
                        quantity = 0
                except:
                    quantity = 0

                if quantity == 0:
                    cart.pop(product_id, None)
                else:
                    cart[product_id] = quantity

        request.session['cart'] = cart
        request.session.modified = True

        # Recalculate subtotals and total
        total = 0
        for pid, qty in cart.items():
            product = Product.objects.get(id=pid)  # Adjust import & error handling
            subtotal = product.price * qty
            subtotals[pid] = f"{subtotal:.2f}"
            total += subtotal

        # Update the total price in session (after recalculating)
        request.session['total_price'] = "%.2f" % total
        request.session.modified = True

        return JsonResponse({'subtotals': subtotals, 'total': f"{total:.2f}"})

    return JsonResponse({'error': 'Invalid request'}, status=400)



def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    # Recalculate total and update session
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': "%.2f" % subtotal,
            })
        except Product.DoesNotExist:
            continue

    # Update total price in session
    request.session['total_price'] = "%.2f" % total  # Store total price in session
    request.session.modified = True  # Mark session as modified

    context = {
        'products': products,
        'total': "%.2f" % total,
    }
    return render(request, 'checkout.html', context)



stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_view(request):
    total_price = request.session.get('total_price', 0)

    # Debugging: Print out session total to confirm it's correct
    print("Total price from session:", total_price)

    try:
        total_cents = int(float(total_price) * 100)
    except (ValueError, TypeError):
        total_cents = 0

    if total_cents < 50:  # Stripe needs at least 0.50€
        return redirect('cart_detail')

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Your Order',
                    },
                    'unit_amount': total_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cart/'),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        print("Stripe error:", e)
        return redirect('cart_detail')



def payment_success(request):
    return render(request, 'payment_success.html')

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return redirect('cart_detail')


def create_checkout_session(request):
    cart = request.session.get('cart', {})
    YOUR_DOMAIN = 'http://localhost:8000'  # Change in production

    line_items = []

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product.name,
                        'description': product.description if hasattr(product, 'description') else '',
                    },
                    'unit_amount': int(product.price * 100),  # Stripe needs cents
                },
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            continue

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
    except Exception as e:
        print(e)
        return redirect('cart_detail')

    return redirect(checkout_session.url)



def calculate_cart_total(request):
    cart = request.session.get('cart', {})
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total += product.price * quantity
        except Product.DoesNotExist:
            continue

    # Save the total to session
    request.session['total_price'] = "%.2f" % total
    return total


def recipe_list(request):
    recipes = Recipe.objects.all()  # Fetching all recipes
    return render(request, 'recipes.html', {'recipes': recipes})

def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # define this in your settings.py
            fail_silently=False,
        )
        return redirect('contact_success')  # Optional: a success page
    return render(request, 'your_template.html')