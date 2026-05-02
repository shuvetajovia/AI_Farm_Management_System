from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('farmer', 'Farmer'),
        ('agronomist', 'Agronomist'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    farm_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Farm size in acres"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
