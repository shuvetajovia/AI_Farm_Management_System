import os
import sys
import django

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management.settings')
django.setup()

from django.core.files import File
from crops.models import Crop

def update_images():
    # Map crop name to filename (we will look for these in media/crops)
    # The images should be moved to media/crops BEFORE running this script
    image_map = {
        'Wheat': 'wheat_crop.png',
        'Rice': 'rice_crop.png',
        'Maize': 'maize_crop.png',
        'Cotton': 'cotton_crop.png',
        'Sugarcane': 'sugarcane_crop.png',
        'Soybean': 'soybean_crop.png',
        'Tomato': 'tomato_crop.png'
    }
    
    # We assume images are already copied to media/crops manually or via shell
    # But to update the ImageField properly in Django, we often assign the path relative to MEDIA_ROOT
    
    crops = Crop.objects.all()
    print(f"Found {crops.count()} crops.")
    
    for crop in crops:
        if crop.name in image_map:
            filename = image_map[crop.name]
            # Since we are placing files directly into media/crops, we can just set the field to 'crops/filename'
            # IF the file exists there.
            
            # Check if file exists in media/crops (Absolute path check)
            # MEDIA_ROOT is usually base_dir/media
            from django.conf import settings
            file_path = os.path.join(settings.MEDIA_ROOT, 'crops', filename)
            
            if os.path.exists(file_path):
                print(f"Updating {crop.name} with {filename}")
                crop.image = f'crops/{filename}'
                crop.save()
            else:
                print(f"Warning: File {filename} not found in media/crops/ for {crop.name}")
        else:
            print(f"No image mapping found for {crop.name}")

if __name__ == '__main__':
    update_images()
