from django.db.models.base import Model as Model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...permissions import HasAdminAccessPermission


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission,TemplateView):
    template_name = 'dashboard/admin/home.html'
    
    

