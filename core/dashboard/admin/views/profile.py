from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile
from django.contrib import messages
from ..forms import AdminChangePasswordForm,  AdminProfileEditForm, AdminProfileImageForm
from ...permissions import HasAdminAccessPermission



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
    

class AdminProfileImageView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    http_method_names = ['post']
    form_class = AdminProfileImageForm
    success_url = reverse_lazy('dashboard:admin:profile_edit')
    success_message = 'ویرایش نمایه با  موفقیت انجام شد.'
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request, 'ارسال عکس با خطا مواجه شد. لطفا مجددا تلاش کنید.')
        return redirect(self.success_url)