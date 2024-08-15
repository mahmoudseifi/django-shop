from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.urls import reverse_lazy
from shop.models import ProductWishlistModel, ProductStatusType
from ...permissions import HasCustomerAccessPermission

class CustomerWishListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = 'dashboard/customer/wishlists/wishlist_list.html'
    paginate_by = 8
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = ProductWishlistModel.objects.filter(user=self.request.user, product__status=ProductStatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(product_title__icontains=search_q)
        if order_by := self.request.GET.get('order_by'):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context
    
    
class CustomerWishlistDeleteView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("dashboard:customer:wishlist_list")
    success_message = "آیتم مورد نظر با موفقیت حذف شد."
    
    def get_queryset(self):
        return ProductWishlistModel.objects.filter(user=self.request.user, product__status=ProductStatusType.publish.value)