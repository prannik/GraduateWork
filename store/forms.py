from django import forms
from .models import Product, ProductComment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'image',
            'price',
            'category'
        ]


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = [
            'text'
        ]

