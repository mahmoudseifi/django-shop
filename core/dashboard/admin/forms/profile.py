from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from django import forms
from accounts.models import Profile

class AdminChangePasswordForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("پسوردهای جدید وارد شده مشابه نیستند."),
        "password_incorrect": _("پسورد فعلی را بدرستی وارد کنید."),
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control text-center', 'placeholder':'پسورد فعلی خود را وارد کنید'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control text-center', 'placeholder':'پسورد جدید را وارد کنید'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control text-center', 'placeholder':'پسورد جدید را دوباره وارد کنید'})
   
    
class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control text-center'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control text-center'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control text-center'})   
        

class AdminProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']