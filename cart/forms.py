from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Количество:', min_value=1, max_value=25)
        #, choices=PRODUCT_QUANTITY_CHOICES, coerce=int,
    # widget=forms.Select(
    #     attrs={'class': 'form-control'}
    #     ))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)