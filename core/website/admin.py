from django.contrib import admin
from .models import ContactModel, NewsLetterModel

@admin.register(ContactModel)
class ContactModelModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'created_date']
    
@admin.register(NewsLetterModel)
class NewsLetterModelModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'created_date']