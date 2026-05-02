import os
import django
import shutil

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management.settings')
django.setup()

from django.conf import settings
from inventory.models import Product
from crops.models import Crop

ARTIFACTS_DIR = r'C:\Users\Om\.gemini\antigravity\brain\e309ed80-24fb-40a6-9aea-3e7c8d2c6b2a'

def copy_image(source, dest_rel):
    src_path = os.path.join(ARTIFACTS_DIR, source)
    dest_path = os.path.join(settings.MEDIA_ROOT, dest_rel)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {source} to {dest_rel}")
    else:
        print(f"WARNING: File not found: {src_path}")

def modify_db():
    print("--- Fixing broken fixture products ---")
    broken_products = [
        ('Urea Fertilizer', 'urea_fertilizer_1774542602386.png', 'products/urea_fertilizer.png'),
        ('Rice Seeds', 'rice_seeds_1774542620478.png', 'products/rice_seeds.png'),
    ]
    for name, src, dest in broken_products:
        copy_image(src, dest)
        try:
            prod = Product.objects.get(name=name)
            prod.image = dest
            prod.save()
            print(f"Updated {name}")
        except Product.DoesNotExist:
            print(f"Product {name} not found in DB.")
            
    print("--- Adding 4 new products ---")
    new_products = [
        {
            'name': 'Heavy Duty Tractor', 'product_type': 'equipment',
            'description': 'A modern green 60HP agricultural tractor for heavy field operations.',
            'price': '650000.00', 'unit': 'unit', 'stock_quantity': 2,
            'image_source': 'tractor_1774542682532.png', 'image_dest': 'products/tractor.png'
        },
        {
            'name': 'Smart Drip Irrigation Kit', 'product_type': 'equipment',
            'description': 'Advanced drip irrigation kit covering up to 1 acre of land, conserves water.',
            'price': '15500.00', 'unit': 'kit', 'stock_quantity': 15,
            'image_source': 'drip_irrigation_1774542704212.png', 'image_dest': 'products/drip_irrigation.png'
        },
        {
            'name': 'NPK 19-19-19 Fertilizer', 'product_type': 'fertilizer',
            'description': 'Balanced NPK complex fertilizer providing essential nutrients for all crop stages.',
            'price': '1250.00', 'unit': 'bag', 'stock_quantity': 80,
            'image_source': 'npk_fertilizer_1774542768233.png', 'image_dest': 'products/npk_fertilizer.png'
        },
        {
            'name': 'Premium Organic Compost', 'product_type': 'fertilizer',
            'description': 'Enriched organic compost to improve soil structure and microbial activity.',
            'price': '350.00', 'unit': 'bag', 'stock_quantity': 120,
            'image_source': 'organic_compost_1774542790723.png', 'image_dest': 'products/organic_compost.png'
        }
    ]
    for item in new_products:
        copy_image(item['image_source'], item['image_dest'])
        Product.objects.get_or_create(
            name=item['name'],
            defaults={
                'product_type': item['product_type'],
                'description': item['description'],
                'price': item['price'],
                'unit': item['unit'],
                'stock_quantity': item['stock_quantity'],
                'image': item['image_dest']
            }
        )
        print(f"Created new product: {item['name']}")

    print("--- Adding 3 new crops ---")
    new_crops = [
        {
            'name': 'Potato', 'season': 'rabi',
            'nitrogen_requirement': 50, 'phosphorus_requirement': 30, 'potassium_requirement': 40,
            'image_source': 'potato_crop_1774542639025.png', 'image_dest': 'crops/potato_crop.png'
        },
        {
            'name': 'Onion', 'season': 'rabi',
            'nitrogen_requirement': 35, 'phosphorus_requirement': 20, 'potassium_requirement': 30,
            'image_source': 'onion_crop_1774542725592.png', 'image_dest': 'crops/onion_crop.png'
        },
        {
            'name': 'Barley', 'season': 'rabi',
            'nitrogen_requirement': 40, 'phosphorus_requirement': 15, 'potassium_requirement': 20,
            'image_source': 'barley_crop_1774542812853.png', 'image_dest': 'crops/barley_crop.png'
        }
    ]
    for item in new_crops:
        copy_image(item['image_source'], item['image_dest'])
        Crop.objects.get_or_create(
            name=item['name'],
            defaults={
                'season': item['season'],
                'nitrogen_requirement': item['nitrogen_requirement'],
                'phosphorus_requirement': item['phosphorus_requirement'],
                'potassium_requirement': item['potassium_requirement'],
                'image': item['image_dest']
            }
        )
        print(f"Created new crop: {item['name']}")
        
    print(f"Current Total Products: {Product.objects.count()}")
    print(f"Current Total Crops: {Crop.objects.count()}")

if __name__ == "__main__":
    modify_db()
