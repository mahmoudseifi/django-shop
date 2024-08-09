from django.core.exceptions import ValidationError
import re
import os

def validate_iranian_cellphone_number(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid Iranian cellphone number.")
    
    

def validate_image_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError('Unsupported file extension. Only .jpg and .jpeg files are allowed.')

def validate_image_size(file):
    if file.size > 100 * 1024:  # 100 KB
        raise ValidationError('File size is too large. The size limit is 100 KB.')