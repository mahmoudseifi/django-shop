from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import ReviewModel
from .forms import SubmitReviewForm

class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = ReviewModel
    form_class = SubmitReviewForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data['product']
        messages.success(self.request, 'نظر شما با  موفقیت ثبت و در انتظار تایید قرار گرفت.')
        return redirect(reverse_lazy('shop:product_detail', kwargs={'slug':product.slug}))
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request,error)
        return redirect(self.request.META.get('HTTP_REFERER'))
    
    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)
    
