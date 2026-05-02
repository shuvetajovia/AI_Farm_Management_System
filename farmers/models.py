from django.db import models
from django.conf import settings

class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    farm_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Farm size in acres"
    )

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def total_land_area(self):
        from django.db.models import Sum
        total = self.lands.aggregate(total=Sum('area'))['total']
        return total if total else 0



class Land(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='lands')
    name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    SOIL_CHOICES = [
        ('Alluvial', 'Alluvial Soil'),
        ('Black', 'Black Soil (Regur)'),
        ('Red', 'Red Soil'),
        ('Laterite', 'Laterite Soil'),
        ('Desert', 'Desert / Arid Soil'),
        ('Forest', 'Forest / Mountain Soil'),
        ('Saline', 'Saline / Alkaline Soil'),
        ('Peaty', 'Peaty / Marshy Soil'),
        ('Loamy', 'Loamy Soil'),
        ('Clay', 'Clay Soil'),
        ('Sandy', 'Sandy Soil'),
    ]
    soil_type = models.CharField(max_length=50, choices=SOIL_CHOICES)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.farmer.user.username}"


class GovernmentResource(models.Model):
    CATEGORY_CHOICES = [
        ('portal', 'Government Agriculture Portal'),
        ('helpline', 'Helpline & Emergency'),
        ('email', 'Official Contact Email'),
        ('insurance', 'Insurance & Subsidy'),
        ('advisory', 'Weather & Advisory'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, help_text='One line description')
    website_url = models.URLField(blank=True, null=True)
    helpline_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']

    is_deleted = models.BooleanField(default=False)
