from django.db import models

from shop.models import Product


class Order (models.Model):
    first_name = models.CharField(max_length=60, verbose_name='Фамилия', blank=True, null=True)
    last_name = models.CharField(max_length=60, verbose_name='Имя', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', blank=True, null=True)
    postal_code = models.CharField(max_length=30, verbose_name='Индекс', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False) 

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

