from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AuthenticationForm(auth_forms.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError("This user is not verified.")
        
    error_messages = {
        "invalid_login": _(
            "لطفا ایمیل یا پسورد خود را بدرستی وارد کنید. "
        ),
    }
