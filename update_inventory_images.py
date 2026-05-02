
import os
import sys
import django

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management.settings')
django.setup()

from inventory.models import Product

def update_inventory_images():
    print("Updating inventory images...")
    
    # Define mapping of produce_type to image filename
    # Based on choices: 'seed', 'fertilizer', 'pesticide', 'equipment', 'fuel'
    image_mapping = {
        'seed': 'inventory/seed.png',
        'fertilizer': 'inventory/fertilizer.png',
        'pesticide': 'inventory/pesticide.png',
        'equipment': 'inventory/equipment.png',
        'fuel': 'inventory/fuel.png'
    }

    products = Product.objects.all()
    count = 0
    
    for product in products:
        if product.product_type in image_mapping:
            image_path = image_mapping[product.product_type]
            print(f"Updating {product.name} ({product.product_type}) -> {image_path}")
            product.image = image_path
            product.save()
            count += 1
            
    print(f"Successfully updated image for {count} products.")

if __name__ == "__main__":
    update_inventory_images()
