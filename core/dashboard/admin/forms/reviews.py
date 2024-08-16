from django import forms
from review.models import ReviewModel

class AdminReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['rate', 'description', 'status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rate'].widget.attrs.update({'class': 'form-control text-center'})
        self.fields['description'].widget.attrs.update({'class': 'form-control text-center'})
        self.fields['status'].widget.attrs.update({'class': 'form-control text-center'})   