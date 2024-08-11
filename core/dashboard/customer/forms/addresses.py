from django import forms
from order.models import AddressUserModel

class AddressUserForm(forms.ModelForm):
    class Meta:
        model = AddressUserModel
        fields = (
            'address',
            'state',
            'city',
            'zip_code',
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})  
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})  