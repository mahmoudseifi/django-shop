from django.urls import path
from .. import views


urlpatterns = [
    path('product/list/', views.AdminProductListView.as_view(), name='product_list'),
    path('product/create/', views.AdminProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', views.AdminProductEditView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.AdminProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/image/add/', views.AdminProductAddImageView.as_view(), name='product_add_image'),
    path('product/<int:pk>/image/<int:image_id>/delete/', views.AdminProductDeleteImageView.as_view(), name='product_delete_image'),
    
]