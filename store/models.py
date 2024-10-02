from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Модель для категорий товаров."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель для товаров."""
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Модель для корзины пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Корзина {self.user.username}'

class CartItem(models.Model):
    """Модель для элементов в корзине."""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'

class Order(models.Model):
    """Модель для заказов."""
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('completed', 'Завершён'),
        ('canceled', 'Отменён'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Заказ {self.id} от {self.user.username}'
