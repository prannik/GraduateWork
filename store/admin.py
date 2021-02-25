from django.contrib import admin
from .models import Product, ProductComment, Category, ProductReview


admin.site.register(Product)
admin.site.register(ProductComment)
admin.site.register(Category)
admin.site.register(ProductReview)
