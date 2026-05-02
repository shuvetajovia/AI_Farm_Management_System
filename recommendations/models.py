from django.db import models
from farmers.models import Land
from crops.models import Crop

class FertilizerRecommendation(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    date_recommended = models.DateField(auto_now_add=True)
    nitrogen_recommended = models.DecimalField(max_digits=5, decimal_places=2)
    phosphorus_recommended = models.DecimalField(max_digits=5, decimal_places=2)
    potassium_recommended = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Recommendation for {self.land.name} - {self.crop.name}"

class CropRecommendation(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    recommended_crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    date_recommended = models.DateField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f"Crop recommendation for {self.land.name}"
