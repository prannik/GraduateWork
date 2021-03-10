from django.contrib import admin
from .models import Product, ProductCategory, ProductReview, Basket, ProductInBasket


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductCategory, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display =['name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


admin.site.register(ProductReview)
admin.site.register(Basket)
admin.site.register(ProductInBasket)
