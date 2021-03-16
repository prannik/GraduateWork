from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [
            'text_1',
            'text_2',
            'text_3',
            'mark',
        ]