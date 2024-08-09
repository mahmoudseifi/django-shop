from django.urls import path
from .. import views


urlpatterns = [
    path('product/list/', views.AdminProductListView.as_view(), name='product_list'),
    path('product/create/', views.AdminProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', views.AdminProductEditView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.AdminProductDeleteView.as_view(), name='product_delete'),
]