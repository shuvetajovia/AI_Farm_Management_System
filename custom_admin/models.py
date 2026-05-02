from django.db import models
from django.conf import settings

class AdminLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Soft Deleted'),
        ('RESTORE', 'Restored'),
        ('PERM_DELETE', 'Permanently Deleted'),
        ('EXPORT', 'Exported Data'),
    ]

    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, null=True, blank=True)
    object_repr = models.CharField(max_length=255, help_text="String representation of object")
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_user} - {self.action} - {self.model_name}"

    class Meta:
        ordering = ['-timestamp']
