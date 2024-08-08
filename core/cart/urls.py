from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('session/add-product/', views.SessionAddProductView.as_view(), name ='session_add_product'),
    path('session/add-product-with-quantity/', views.SessionAddProductWithQuantityView.as_view(), name ='session_add_product_with_quantity'),
    path('session/update-product-quantity/', views.SessionUpdateProductQuantityView.as_view(), name ='session_update_product_quantity'),
    path('session/remove-product/', views.SessionRemoveProductView.as_view(), name ='session_remove_product'),
    path('session/cart/summary/', views.SessionCartSummaryView.as_view(), name='session_cart_summary'),
]