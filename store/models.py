from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=48)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title}'


class ProductComment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=48)

    def __str__(self):
        return f'{self.name}'


# class Like(models.Model):
#     LIKE_OR_DISLAKE_CHOICES = (
#         ("LIKE", "like"),
#         ("DISLIKE", "dislike"),
#         (None, "None")
#     )
#
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     for_product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     like_or_dislike = models.CharField(max_length=7,
#                                        choices=LIKE_OR_DISLAKE_CHOICES,
#                                        default=None)


class ProductReview(models.Model):
    mark = models.IntegerField(default=5)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)