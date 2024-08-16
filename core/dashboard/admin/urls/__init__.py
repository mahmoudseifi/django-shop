from django.urls import path, include


app_name = 'admin'

urlpatterns = [
    path('', include('dashboard.admin.urls.generals')),
    path('', include('dashboard.admin.urls.profile')),
    path('', include('dashboard.admin.urls.products')),
    path('', include('dashboard.admin.urls.coupons')),
     path('', include('dashboard.admin.urls.reviews')), 

]