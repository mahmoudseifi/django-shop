from django import forms
from django_flatpickr.widgets import DatePickerInput
from order.models import CouponModel

class AdminCouponForm(forms.ModelForm):
    expiration_date = forms.DateField(
        widget=DatePickerInput(
            attrs={
                "class": "datepicker",
                "data-enable-time": "false",
                "data-date-format": "Y-m-d",
            }
        )
    )
    class Meta:
        model = CouponModel
        fields = (
            'code',
            'discount_percent',
            'max_limit_usage',
            'expiration_date',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'class': 'form-control is-valid'})
        self.fields['discount_percent'].widget.attrs.update({'class': 'form-control is-valid'})
        self.fields['max_limit_usage'].widget.attrs.update({'class': 'form-control is-valid'})   
        self.fields['expiration_date'].widget = DatePickerInput(attrs={'class': 'form-control is-valid', 'type':'date'}) 
        
