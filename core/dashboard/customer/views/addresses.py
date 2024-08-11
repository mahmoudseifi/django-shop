from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from ..forms import AddressUserForm
from ...permissions import HasCustomerAccessPermission
from order.models import AddressUserModel


class AddressUserListView(LoginRequiredMixin, HasCustomerAccessPermission,ListView):
    template_name = 'dashboard/customer/addresses/address_list.html'
    
    def get_queryset(self):
        return AddressUserModel.objects.filter(user=self.request.user)

class AddressUserCreateView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, CreateView):
    template_name = 'dashboard/customer/addresses/address_create.html'
    queryset = AddressUserModel.objects.all()
    form_class = AddressUserForm
    success_message = 'ایجاد آدرس با موفقیت انجام شد.'
    success_url = reverse_lazy('dashboard:customer:address_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUserUpdateView(LoginRequiredMixin, HasCustomerAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/customer/addresses/address_edit.html'
    queryset = AddressUserModel.objects.all()
    form_class = AddressUserForm
    success_message = 'ویرایش آدرس با موفقیت انجام شد.'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:customer:address_edit',kwargs={'pk': self.get_object().pk})


class AddressUserDeleteView(LoginRequiredMixin, HasCustomerAccessPermission,SuccessMessageMixin, DeleteView):
    template_name = 'dashboard/customer/addresses/address_delete.html'
    queryset = AddressUserModel.objects.all()
    success_url = reverse_lazy('dashboard:customer:address_list')
    success_message = 'حذف آدرس با موفقیت انجام شد.'