from django.urls import path
from .. import views


urlpatterns = [
    path('order-list/', views.CustomerOrderListView.as_view(), name='customer_order_list'),
    path('order-detail/<int:pk>/detail/', views.CustomerOrderDetailView.as_view(), name='customer_order_detail'),
    path('invoice/<int:pk>/', views.CustomerInvoiceView.as_view(), name='customer_invoice'),
]