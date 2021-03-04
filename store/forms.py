from django import forms
from .models import Product, ProductReview


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'price',
            'category',
        ]


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [
            'text_1',
            'text_2',
            'text_3',
            'mark',
        ]

