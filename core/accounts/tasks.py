from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

@shared_task
def send_password_reset_email(user_id, domain, uid, token):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    mail_subject = 'Reset your password'
    message = render_to_string('registration/password_reset_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])