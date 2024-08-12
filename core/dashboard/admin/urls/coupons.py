from django.urls import path
from .. import views


urlpatterns = [
    path('coupon/list/', views.AdminCouponListView.as_view(), name='coupon_list'),
    path('coupon/create/', views.AdminCouponCreateView.as_view(), name='coupon_create'),
    path('coupon/<int:pk>/edit/', views.AdminCouponEditView.as_view(), name='coupon_edit'),
    path('coupon/<int:pk>/delete/', views.AdminCouponDeleteView.as_view(), name='coupon_delete'),
]