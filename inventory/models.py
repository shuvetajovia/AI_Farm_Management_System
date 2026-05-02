from django.db import models

class Product(models.Model):
    PRODUCT_TYPES = [
        ('seed', 'Seed'),
        ('crop', 'Crop'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('equipment', 'Equipment'),
        ('fuel', 'Fuel'),
    ]
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')  # kg, liters, etc.
    stock_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # For placeholder images

    def __str__(self):
        return f"{self.name} ({self.product_type})"

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level

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
