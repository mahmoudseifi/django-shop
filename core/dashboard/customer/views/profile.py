from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile
from django.contrib import messages
from ..forms import CustomerChangePasswordForm,  CustomerProfileEditForm, CustomerProfileImageForm
from ...permissions import HasCustomerAccessPermission



class CustomerDashboardSecurityView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, TemplateView, auth_views.PasswordChangeView):
    template_name = 'dashboard/customer/profile/security_edit.html'
    form_class = CustomerChangePasswordForm
    success_url = reverse_lazy('dashboard:customer:security_edit')
    success_message = 'پسورد با موفقیت تغییر کرد.'


class CustomerProfileEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/customer/profile/profile_edit.html'
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy('dashboard:customer:profile_edit')
    success_message = 'ویرایش پروفایل با  موفقیت انجام شد.'
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    

class CustomerProfileImageView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    http_method_names = ['post']
    form_class = CustomerProfileImageForm
    success_url = reverse_lazy('dashboard:customer:profile_edit')
    success_message = 'ویرایش نمایه با  موفقیت انجام شد.'
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request, 'ارسال عکس با خطا مواجه شد. لطفا مجددا تلاش کنید.')
        return redirect(self.success_url)