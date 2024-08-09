from django.urls import path
from .. import views


urlpatterns = [
    path('security/edit/', views.AdminDashboardSecurityView.as_view(), name='security_edit'),
    path('profile/edit/', views.AdminProfileEditView.as_view(), name='profile_edit'),
    path('profile/image/', views.AdminProfileImageView.as_view(), name='profile_image_edit'),
    

]