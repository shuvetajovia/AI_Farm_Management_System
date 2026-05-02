import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management.settings')
django.setup()

from crops.models import Crop

crops_data = [
    {'name': 'Maize', 'season': 'kharif', 'nitrogen_requirement': 60, 'phosphorus_requirement': 24, 'potassium_requirement': 24},
    {'name': 'Cotton', 'season': 'kharif', 'nitrogen_requirement': 40, 'phosphorus_requirement': 20, 'potassium_requirement': 20},
    {'name': 'Sugarcane', 'season': 'kharif', 'nitrogen_requirement': 100, 'phosphorus_requirement': 40, 'potassium_requirement': 40},
    {'name': 'Soybean', 'season': 'kharif', 'nitrogen_requirement': 20, 'phosphorus_requirement': 30, 'potassium_requirement': 20},
    {'name': 'Tomato', 'season': 'rabi', 'nitrogen_requirement': 40, 'phosphorus_requirement': 25, 'potassium_requirement': 25},
]

for cd in crops_data:
    Crop.objects.get_or_create(name=cd['name'], defaults=cd)

import update_crop_images
update_crop_images.update_images()
print("Done creating and updating all crops!")
