from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, verbose_name='Цена', max_digits=10,
                                default=Decimal('0.00'))
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True)
    rating = models.DecimalField(default=Decimal('0.00'), max_digits=3, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name='Нет в наличии')

    def __str__(self):
        return f'{self.name}'


class ProductCategory(models.Model):
    name = models.CharField(max_length=48)

    def __str__(self):
        return f'{self.name}'


class ProductReview(models.Model):
    MARK_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text_1 = models.TextField(max_length=500, verbose_name='Отзыв')
    text_2 = models.TextField(max_length=200, blank=True, null=True, verbose_name='Плюсы')
    text_3 = models.TextField(max_length=200, blank=True, null=True,  verbose_name='Минусы')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    mark = models.CharField(max_length=4, choices=MARK_CHOICES)

    def __str__(self):
        return f'{self.author} - {self.product}'


class ProductReviewLike(models.Model):
    LIKE_OR_DISLAKE_CHOICES = (
        ("LIKE", "like"),
        ("DISLIKE", "dislike"),
        (None, "None")
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    for_review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    like_or_dislike = models.CharField(max_length=7,
                                       choices=LIKE_OR_DISLAKE_CHOICES,
                                       default=None)
    

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

class ProductInBasket(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_of_product = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.basket}'
