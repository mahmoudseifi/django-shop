from django.db import models
from accounts.validators import validate_iranian_cellphone_number


class ContactModel(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, validators=[validate_iranian_cellphone_number], blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    
class NewsLetterModel(models.Model):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email