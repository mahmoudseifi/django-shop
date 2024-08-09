from django import forms
from shop.models import ProductModel
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdminProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = [
            'category',
            'title',
            'slug',
            'image',
            'description',
            'breif_description',
            'stock',
            'status',
            'price',
            'discount_percent',
        ]
        widgets = {
            'description': CKEditorUploadingWidget(),
            'breif_description': CKEditorUploadingWidget(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select is-valid'})
        self.fields['title'].widget.attrs.update({'class': 'form-control is-valid'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control is-valid'})   
        self.fields['image'].widget.attrs.update({'class': 'form-control is-valid', 'type':'file'})   
        self.fields['description'].widget.attrs.update({'class': 'form-control'})   
        self.fields['breif_description'].widget.attrs.update({'class': 'form-control'})   
        self.fields['stock'].widget.attrs.update({'class': 'form-control is-valid', 'type':'number'})   
        self.fields['status'].widget.attrs.update({'class': 'form-select is-valid'})   
        self.fields['price'].widget.attrs.update({'class': 'form-control is-valid'}) 
        self.fields['discount_percent'].widget.attrs.update({'class': 'form-control is-valid'})  
        
        