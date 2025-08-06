from django import forms

class CategoryFilterForm(forms.Form):
    men = forms.BooleanField(required=False, label="Men")
    women = forms.BooleanField(required=False, label="Women")
    accessories = forms.BooleanField(required=False, label="Accessories")


class PriceFilterForm(forms.Form):
    zero_to_fifty = forms.BooleanField(required=False, label="$0 - $50")
    fifty_to_hundred = forms.BooleanField(required=False, label="$51 - $100")
    hundred_plus = forms.BooleanField(required=False, label="$101+")