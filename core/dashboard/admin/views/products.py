from django.db.models.base import Model as Model
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import FieldError
from shop.models import ProductModel, ProductCategoryModel, ProductImageModel
from ..forms import AdminProductForm, ProductImageForm
from ...permissions import HasAdminAccessPermission



class AdminProductListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = 'dashboard/admin/products/product_list.html'
    paginate_by = 9
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = ProductModel.objects.all()
        if search_q:=self.request.GET.get('q'):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id:=self.request.GET.get('category_id'):
            queryset = queryset.filter(category__id=category_id)
        if min_price:=self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)
        if max_price:=self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get('order_by'):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['categories'] = ProductCategoryModel.objects.all()
        return context


class AdminProductCreateView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, CreateView):
    template_name = 'dashboard/admin/products/product_create.html'
    queryset = ProductModel.objects.all()
    form_class = AdminProductForm
    success_message = 'ایجاد محصول با موفقیت انجام شد.'
    success_url = reverse_lazy('dashboard:admin:product_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class AdminProductEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/products/product_edit.html'
    queryset = ProductModel.objects.all()
    form_class = AdminProductForm
    success_message = 'ویرایش محصول با موفقیت انجام شد.'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product_edit',kwargs={'pk': self.get_object().pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ProductImageForm()
        return context
    

class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, DeleteView):
    template_name = 'dashboard/admin/products/product_delete.html'
    queryset = ProductModel.objects.all()
    success_url = reverse_lazy('dashboard:admin:product_list')
    success_message = 'حذف محصول با موفقیت انجام شد.'
    

class AdminProductAddImageView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, CreateView):
    http_method_names = ['post']
    form_class = ProductImageForm
    success_message = 'تصویر با موفقیت بارگذاری شد.'
    
    def get_queryset(self):
        return ProductImageModel.objects.filter(product__id=self.kwargs.get('pk'))
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product_edit',kwargs={'pk': self.kwargs.get('pk')})
    
    def form_valid(self, form):
        form.instance.product = ProductModel.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'ارسال تصویر با مشکل مواجه شد.')
        return redirect(reverse_lazy('dashboard:admin:product_edit',kwargs={'pk': self.kwargs.get('pk')}))
    
    

class AdminProductDeleteImageView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, DeleteView):
    http_method_names = ['post']
    model = ProductImageModel
    success_message = 'تصویر با موفقیت حذف شد.'
    
    
    def get_object(self, queryset=None):
        return get_object_or_404(ProductImageModel, id=self.kwargs.get('image_id'), product__id=self.kwargs.get('pk') )
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product_edit',kwargs={'pk': self.kwargs.get('pk')})
    

    