import os
import django
import shutil

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management.settings')
django.setup()

from django.conf import settings
from inventory.models import Product

# Definitions
ARTIFACTS_DIR = r'C:\Users\Om\.gemini\antigravity\brain\e309ed80-24fb-40a6-9aea-3e7c8d2c6b2a'

PRODUCT_DATA = [
    {
        'name': 'Premium Organic Wheat Seed',
        'product_type': 'seed',
        'description': 'High-yield premium organic wheat seeds, perfect for winter and spring planting. Resilient to common pests.',
        'price': '850.00',
        'unit': 'kg',
        'stock_quantity': 500,
        'image_source': 'premium_wheat_seed_1774540917515.png',
        'image_dest': 'products/wheat_seed.png'
    },
    {
        'name': 'Smart Soil Sensor V2',
        'product_type': 'equipment',
        'description': 'IoT enabled smart soil sensor. Monitors NPK levels, moisture, and temperature. Syncs with smart agriculture dashboard.',
        'price': '3499.00',
        'unit': 'unit',
        'stock_quantity': 50,
        'image_source': 'smart_soil_sensor_1774540877582.png',
        'image_dest': 'products/smart_sensor.png'
    },
    {
        'name': 'Bio-Organic Liquid Fertilizer',
        'product_type': 'fertilizer',
        'description': '100% organic liquid fertilizer packed with essential micronutrients for faster crop growth and better yields.',
        'price': '450.00',
        'unit': 'liters',
        'stock_quantity': 200,
        'image_source': 'bio_organic_fertilizer_1774540936466.png',
        'image_dest': 'products/liquid_fertilizer.png'
    },
    {
        'name': 'SafeCrop Neem Pesticide',
        'product_type': 'pesticide',
        'description': 'Eco-friendly neem-based pesticide. Safely eliminates harmful pests without damaging the crop or soil health.',
        'price': '320.00',
        'unit': 'liters',
        'stock_quantity': 150,
        'image_source': 'safecrop_pesticide_1774540956537.png',
        'image_dest': 'products/neem_pesticide.png'
    }
]

def populate():
    print("Starting product ingestion...")
    target_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    os.makedirs(target_dir, exist_ok=True)
    
    Product.objects.all().delete()
    
    for item in PRODUCT_DATA:
        src_path = os.path.join(ARTIFACTS_DIR, item['image_source'])
        dest_path = os.path.join(settings.MEDIA_ROOT, item['image_dest'])
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied image for {item['name']}")
        else:
            print(f"Warning: Image {src_path} not found.")

        Product.objects.create(
            name=item['name'],
            product_type=item['product_type'],
            description=item['description'],
            price=item['price'],
            unit=item['unit'],
            stock_quantity=item['stock_quantity'],
            image=item['image_dest']
        )
        print(f"Created product: {item['name']}")
        
    print(f"Total Products in DB: {Product.objects.count()}")

if __name__ == '__main__':
    populate()
