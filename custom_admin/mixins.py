from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.role == 'admin')

    def handle_no_permission(self):
        messages.error(self.request, "Access Denied: Super Admin privileges required.")
        return redirect('custom_admin:dashboard')

class ManagerAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.role in ['admin', 'manager'])

    def handle_no_permission(self):
        messages.error(self.request, "Access Denied: Admin privileges required.")
        return redirect('accounts:login')
