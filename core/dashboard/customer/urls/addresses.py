from django.urls import path
from .. import views


urlpatterns = [
    path('address/list/', views.AddressUserListView.as_view(), name='address_list'),
    path('address/create/', views.AddressUserCreateView.as_view(), name='address_create'),
    path('address/<int:pk>/edit/', views.AddressUserUpdateView.as_view(), name='address_edit'),
    path('address/<int:pk>/delete/', views.AddressUserDeleteView.as_view(), name='address_delete'),
]