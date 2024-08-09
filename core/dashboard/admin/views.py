from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile
from .forms import AdminChangePasswordForm,  AdminProfileEditForm
from ..permissions import HasAdminAccessPermission


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission,TemplateView):
    template_name = 'dashboard/admin/home.html'
    
    

class AdminDashboardSecurityView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, TemplateView, auth_views.PasswordChangeView):
    template_name = 'dashboard/admin/profile/security_edit.html'
    form_class = AdminChangePasswordForm
    success_url = reverse_lazy('dashboard:admin:security_edit')
    success_message = 'پسورد با موفقیت تغییر کرد.'


class AdminProfileEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/profile/profile_edit.html'
    form_class = AdminProfileEditForm
    success_url = reverse_lazy('dashboard:admin:profile_edit')
    success_message = 'ویرایش پروفایل با  موفقیت انجام شد.'
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)