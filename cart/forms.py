from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Количество:', min_value=1, max_value=25)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
