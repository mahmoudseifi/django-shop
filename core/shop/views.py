
from django.views.generic import (
    ListView,
    DetailView,
    View
)
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from review.models import ReviewModel, ReviewStatusType
from .models import ProductModel, ProductStatusType, ProductCategoryModel, ProductWishlistModel


class ShopProductGridView(ListView):
    template_name = 'shop/products_grid.html'
    paginate_by = 9

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = ProductModel.objects.filter(
            status=ProductStatusType.publish.value)
        if search_q := self.request.GET.get('q'):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get('category_id'):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get('max_price'):
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
        context['wishlist_items'] = ProductWishlistModel.objects.filter(user=self.request.user).values_list(
            'product__id', flat=True) if self.request.user.is_authenticated else []
        context['categories'] = ProductCategoryModel.objects.all()
        return context


class ShopProductDetailView(DetailView):
    template_name = 'shop/products_detail.html'
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['reviews'] = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted.value)
        context['is_wished'] = ProductWishlistModel.objects.filter(
            user=self.request.user, product__id=product.id).exists() if self.request.user.is_authenticated else False
        return context


class AddOrRemoveWishListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        message = ''

        if product_id:
            try:
                wishlist_item = ProductWishlistModel.objects.get(
                    user=request.user, product__id=product_id)
                wishlist_item.delete()
                message = 'آیتم مورد نظر از لیست علایق حذف شد'
            except ProductWishlistModel.DoesNotExist:
                ProductWishlistModel.objects.create(
                    user=request.user, product_id=product_id)
                message = 'آیتم مورد نظر به لیست علایق اضافه شد'
        return JsonResponse({'message': message})
