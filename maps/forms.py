from django import forms

from maps.models import Address


class CreateDatasetForm(forms.Form):
    address = forms.URLField(required=True, max_length=400, widget=forms.URLInput(
        attrs={"class": "input", "placeholder": "Write address here"}))

    class Meta:
        model = Address
        fields = 'address'

