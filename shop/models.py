import os
from decimal import Decimal
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])
    

def get_upload_path(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]  
    return os.path.join('static/images/', filename)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', 
        on_delete=models.CASCADE
        )
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True)
    rating = models.DecimalField(default=Decimal('0.00'), max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('slug',),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

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
    text_3 = models.TextField(max_length=200, blank=True, null=True, verbose_name='Минусы')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    mark = models.CharField(max_length=4, choices=MARK_CHOICES)

    class Meta:
        ordering = ('product', 'mark')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

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
