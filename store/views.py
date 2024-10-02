from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def index(request):
    """Главная страница магазина."""
    return render(request, 'store/index.html')

def product_list(request):
    """Список всех товаров."""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    """Детали конкретного товара."""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart_view(request):
    """Просмотр корзины пользователя."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('store:cart')

@login_required
def checkout(request):
    """Оформление заказа."""
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(user=request.user)
    for item in cart.items.all():
        order.products.add(item.product)
    cart.items.all().delete()  # Очищаем корзину после оформления заказа
    return render(request, 'store/checkout.html', {'order': order})

@login_required
def order_history(request):
    """История заказов пользователя."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

def register(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def profile(request):
    """Профиль пользователя."""
    return render(request, 'store/profile.html')

def login_view(request):
    """Вход пользователя."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store:product_list') 
            else:
                return render(request, 'registration/login.html', {'form': form, 'errors': 'Неверное имя пользователя или пароль'})
        else:
            return render(request, 'registration/login.html', {'form': form, 'errors': form.errors})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
