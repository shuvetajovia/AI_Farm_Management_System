from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=50, choices=[
        ('kharif', 'Kharif'),
        ('rabi', 'Rabi'),
        ('zaid', 'Zaid'),
    ])
    description = models.TextField(blank=True)
    optimal_ph_min = models.DecimalField(max_digits=4, decimal_places=2, default=6.0)
    optimal_ph_max = models.DecimalField(max_digits=4, decimal_places=2, default=7.5)
    nitrogen_requirement = models.DecimalField(max_digits=5, decimal_places=2, help_text="N in kg/acre")
    phosphorus_requirement = models.DecimalField(max_digits=5, decimal_places=2, help_text="P in kg/acre")
    potassium_requirement = models.DecimalField(max_digits=5, decimal_places=2, help_text="K in kg/acre")
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # For placeholder images

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        """Return image URL for display, preferring uploaded image over placeholder"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        else:
            return '/static/images/no-image.png'  # Default placeholder

    is_deleted = models.BooleanField(default=False)
