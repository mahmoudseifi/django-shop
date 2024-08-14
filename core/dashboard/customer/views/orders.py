from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404
from order.models import OrderModel
from ...permissions import HasCustomerAccessPermission

class CustomerOrderListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = 'dashboard/customer/orders/customer_order_list.html'
    paginate_by = 5
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = OrderModel.objects.filter(user=self.request.user)
        if status_orders:=self.request.GET.get('status_orders'):
            queryset = queryset.filter(status=status_orders)
        if order_by := self.request.GET.get('order_by'):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        
        return queryset
    
    
    
class CustomerOrderDetailView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    template_name = 'dashboard/customer/orders/customer_order_detail.html'
    
    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
    

class CustomerInvoiceView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    template_name = 'dashboard/customer/orders/customer_invoice.html'
    
    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)