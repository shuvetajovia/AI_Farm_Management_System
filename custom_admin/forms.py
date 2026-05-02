from django import forms
from accounts.models import CustomUser

class AdminUserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'})
        }
