import os
import django
import shutil

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management.settings')
django.setup()

from django.conf import settings
from inventory.models import Product

# Directory where we will check for source images (the ones in artifacts or previously generated)
# Note: I'll trust the agent to place them here or I will assume they are in the artifacts dir
# But for now, I will define the target directory which is what matters for Django
TARGET_DIR = os.path.join(settings.MEDIA_ROOT, 'products')
os.makedirs(TARGET_DIR, exist_ok=True)

# Map product types to image filenames (assuming we have these standard names)
PRODUCT_IMAGES = {
    'seed': 'seed_product.png',
    'fertilizer': 'fertilizer.png', # Note: filenames might need to be flexible or we just copy what we have
    'pesticide': 'pesticide.png',
    'equipment': 'equipment.png',
    'fuel': 'fuel.png'
}

# Correct filenames based on what I see in list_dir output from previous steps
# The agent previously generated:
# seed_product_1768491830237.png
# fertilizer_product_1768491848998.png
# pesticide_product_1768491869835.png
# equipment_product_1768491902411.png
# fuel_product_1768491919526.png

# I will use these specific source files from the artifacts directory
ARTIFACTS_DIR = r'C:\Users\jadha\.gemini\antigravity\brain\ea1e5cf2-53f9-4db5-94a7-ddf9a717745e'

SOURCE_MAP = {
    'seed': 'seed_product_1768491830237.png',
    'fertilizer': 'fertilizer_product_1768491848998.png',
    'pesticide': 'pesticide_product_1768491869835.png',
    'equipment': 'equipment_product_1768491902411.png',
    'fuel': 'fuel_product_1768491919526.png'
}

def update_images():
    count = 0
    print(f"Updating inventory images...")
    
    # 1. Copy images to media/products/
    for p_type, src_filename in SOURCE_MAP.items():
        src_path = os.path.join(ARTIFACTS_DIR, src_filename)
        # Clean destination filename
        dest_filename = src_filename.split('_product_')[0] + '.png' # e.g. seed.png
        if 'product' in src_filename and 'product' not in dest_filename and p_type == 'seed':
             dest_filename = 'seed_product.png'
        
        # Simpler naming for cleaner URLs
        dest_filename = f"{p_type}.png" 
        
        dest_path = os.path.join(TARGET_DIR, dest_filename)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_filename} to {dest_path}")
        else:
            print(f"Warning: Source image not found: {src_path}")

    # 2. Update Database
    products = Product.objects.all()
    for product in products:
        # Determine strict image name
        image_name = f"products/{product.product_type}.png"
        
        # Check if file exists in media root
        full_path = os.path.join(settings.MEDIA_ROOT, 'products', f"{product.product_type}.png")
        
        if os.path.exists(full_path):
            product.image = image_name
            product.save()
            print(f"Updated {product.name} ({product.product_type}) -> {image_name}")
            count += 1
        else:
            print(f"Skipping {product.name}: Image not found at {full_path}")

    print(f"Successfully updated {count} products.")

if __name__ == '__main__':
    update_images()
