from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import FieldError
from review.models import ReviewModel, ReviewStatusType
from ..forms import AdminReviewForm
from ...permissions import HasAdminAccessPermission



class AdminReviewListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = 'dashboard/admin/reviews/review_list.html'
    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = ReviewModel.objects.all()
        if search_q:=self.request.GET.get('q'):
            queryset = queryset.filter(product__title__icontains=search_q)
        if status:=self.request.GET.get('status'):
            queryset = queryset.filter(status=status)
        if order_by := self.request.GET.get('order_by'):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_types"] = ReviewStatusType.choices
        return context
    
    
class AdminReviewEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/reviews/review_edit.html'
    queryset = ReviewModel.objects.all()
    form_class = AdminReviewForm
    success_message = 'ویرایش دیدگاه با موفقیت انجام شد.'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:review_edit',kwargs={'pk': self.kwargs.get('pk')})