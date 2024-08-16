from django import forms
from shop.models import ProductModel, ProductStatusType
from .models import ReviewModel

class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['product', 'rate', 'description']
        error_messages = {
            'description': {
                'required': 'فیلد توضیحات اجباری است',
            },
        }
        
    def clean(self):
        clean_date = super().clean()
        product = clean_date.get('product')
        
        try:
            ProductModel.objects.get(id=product.id, status=ProductStatusType.publish.value)
        
        except ProductModel.DoesNotExist:
             raise forms.ValidationError('این محصول وجود ندارد.')
         
        return clean_date