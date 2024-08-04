from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .tasks import send_password_reset_email

User = get_user_model()

class AuthenticationForm(auth_forms.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError("This user is not verified.")

class PasswordResetForm(auth_forms.PasswordResetForm):
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("ایمیلی با این آدرس وجود ندارد. دوباره امتحان کنید.")
        return email
    
