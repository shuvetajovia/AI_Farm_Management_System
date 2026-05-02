from django.db import models
from farmers.models import Land

class SoilData(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='soil_data')
    date_tested = models.DateField()
    ph_level = models.DecimalField(max_digits=4, decimal_places=2)
    nitrogen = models.DecimalField(max_digits=5, decimal_places=2, help_text="N in ppm")
    phosphorus = models.DecimalField(max_digits=5, decimal_places=2, help_text="P in ppm")
    potassium = models.DecimalField(max_digits=5, decimal_places=2, help_text="K in ppm")
    organic_carbon = models.DecimalField(max_digits=5, decimal_places=2, help_text="Organic Carbon %", null=True, blank=True)
    moisture = models.DecimalField(max_digits=5, decimal_places=2, help_text="Moisture %")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_tested']

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Soil data for {self.land.name} on {self.date_tested}"
