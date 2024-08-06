from django import forms
from .models import ContactModel, NewsLetterModel

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactModel
        fields = ['first_name', 'last_name', 'email', 'description', 'phone_number']
        

class NewsLetterForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': 'ایمیل صحیح وارد کنید.'
        }
    )
    class Meta:
        model = NewsLetterModel
        fields = ['email']
       
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and NewsLetterModel.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلا در خبرنامه ثبت نام شده است.')
        return email