from django.contrib.auth import views as auth_views , get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .forms import AuthenticationForm, PasswordResetForm
from .tasks import send_password_reset_email


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

class PasswordResetView(auth_views.PasswordResetView, SuccessMessageMixin):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    form_class = PasswordResetForm
    success_message = "لینک تغییررمز عبور به ایمیل شما ارسال گردید."
    success_url = reverse_lazy('accounts:login')


    def form_valid(self, form):
        # Call the original method to send the email
        response = super().form_valid(form)
        
        # Extract necessary information
        email = form.cleaned_data['email']
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(self.request).domain

            # Call the Celery task
            send_password_reset_email.delay(user.pk, domain, uid, token)
            messages.success(self.request, self.success_message)
        
        return response
    

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView, SuccessMessageMixin):
    template_name = 'accounts/password_reset_confirm.html'
    success_message = "پسورد شما با موفقیت تغییر کرد. اکنون میتوانید وارد شوید."
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    

