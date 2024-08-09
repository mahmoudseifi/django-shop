from django.urls import path
from .. import views


urlpatterns = [
    path('security/edit/', views.CustomerDashboardSecurityView.as_view(), name='security_edit'),
    path('profile/edit/', views.CustomerProfileEditView.as_view(), name='profile_edit'),
    path('profile/image/', views.CustomerProfileImageView.as_view(), name='profile_image_edit'),
    

]