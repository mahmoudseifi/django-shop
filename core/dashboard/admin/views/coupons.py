from django.forms import BaseForm
from django.http.response import HttpResponse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import ProtectedError
from django.contrib import messages
from django.core.exceptions import FieldError
from order.models import CouponModel
from ..forms import AdminCouponForm
from ...permissions import HasAdminAccessPermission



class AdminCouponListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    queryset = CouponModel.objects.all()
    template_name = 'dashboard/admin/coupons/coupon_list.html'
    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = CouponModel.objects.all()
        if search_q:=self.request.GET.get('q'):
            queryset = queryset.filter(code__icontains=search_q)
        if order_by := self.request.GET.get('order_by'):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
class AdminCouponCreateView(LoginRequiredMixin, HasAdminAccessPermission, CreateView):
    template_name = 'dashboard/admin/coupons/coupon_create.html'
    queryset = CouponModel.objects.all()
    form_class = AdminCouponForm
    success_message = 'ایجاد کد تخفیف با موفقیت انجام شد.'
    success_url = reverse_lazy('dashboard:admin:coupon_list')
    
    
    
class AdminCouponEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/coupons/coupon_edit.html'
    queryset = CouponModel.objects.all()
    form_class = AdminCouponForm
    success_message = 'ویرایش کد تخفیف با موفقیت انجام شد.'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:coupon_edit',kwargs={'pk': self.get_object().pk})

class AdminCouponDeleteView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, DeleteView):
    template_name = 'dashboard/admin/coupons/coupon_delete.html'
    queryset = CouponModel.objects.all()
    success_url = reverse_lazy('dashboard:admin:coupon_list')
    success_message = 'حذف کد تخفیف با موفقیت انجام شد.'
    
    def form_valid(self, form):
        try:
            self.get_object().delete()
        except ProtectedError:
            messages.error(self.request, "این کوپن در حال استفاده است و قابل حذف نمی باشد.")
            return self.form_invalid(form)
        return super().form_valid(form)
       