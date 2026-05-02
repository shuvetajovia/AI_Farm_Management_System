
import os
import django

# Set up Django environment manually for script execution
# Assuming script is run from project root or via shell, but let's make it robust
# Correct way: pass this code to 'python manage.py shell' via stdin or save and run

from farmers.models import GovernmentResource

def populate():
    # Clear existing to avoid duplicates if re-run
    # GovernmentResource.objects.all().delete()
    if GovernmentResource.objects.count() > 0:
        print("Resources already exist. Skipping population.")
        return

    resources = [
        # 1. Government Agriculture Portals
        {
            "category": "portal", "name": "e-NAM (National Agriculture Market)",
            "description": "Pan-India electronic trading portal for farm produce.",
            "website_url": "https://www.enam.gov.in", "helpline_number": "1800-270-0224"
        },
        {
            "category": "portal", "name": "PM-KISAN Portal",
            "description": "Direct income support portal for farmers.",
            "website_url": "https://pmkisan.gov.in", "helpline_number": "155261"
        },
        {
            "category": "portal", "name": "Soil Health Card Portal",
            "description": "Official portal for soil health tracking and reports.",
            "website_url": "https://soilhealth.dac.gov.in", "helpline_number": "011-23381385"
        },
        {
            "category": "portal", "name": "MKisan Portal",
            "description": "Unified mobile-based advisory services for farmers.",
            "website_url": "https://mkisan.gov.in", "helpline_number": "1800-180-1551"
        },
        {
            "category": "portal", "name": "Jaivik Kheti Portal",
            "description": "Dedicated portal for organic farming promotion.",
            "website_url": "https://www.jaivikkheti.in", "helpline_number": ""
        },

        # 2. Farmer Helplines & Emergency Contacts
        {
            "category": "helpline", "name": "Kisan Call Center (KCC)",
            "description": "National toll-free helpline for agricultural queries.",
            "website_url": "https://dackkms.gov.in", "helpline_number": "1800-180-1551"
        },
        {
            "category": "helpline", "name": "Agriculture Emergency Helpline",
            "description": "Disaster management control room for crop loss.",
            "website_url": "", "helpline_number": "1077"
        },
        {
            "category": "helpline", "name": "Animal Husbandry Helpline",
            "description": "Support for livestock diseases and care.",
            "website_url": "", "helpline_number": "1962"
        },
        {
            "category": "helpline", "name": "Women Helpline (Kisan)",
            "description": "Dedicated support line for women farmers.",
            "website_url": "", "helpline_number": "181"
        },
        {
            "category": "helpline", "name": "Farm Suicide Prevention",
            "description": "Mental health support for distressed farmers.",
            "website_url": "", "helpline_number": "1800-599-0019"
        },

        # 3. Official Agriculture Emails
        {
            "category": "email", "name": "Ministry of Agriculture Support",
            "description": "General queries for the Ministry.",
            "website_url": "https://agricoop.nic.in", "email": "agri-help@gov.in"
        },
        {
            "category": "email", "name": "PM-KISAN Helpdesk",
            "description": "Email support for payment issues.",
            "website_url": "", "email": "pmkisan-ict@gov.in"
        },
        {
            "category": "email", "name": "e-NAM Technical Support",
            "description": "Technical assistance for trading portal.",
            "website_url": "", "email": "enam.helpdesk@gmail.com"
        },
        {
            "category": "email", "name": "ICAR Info Desk",
            "description": "Scientific queries and research information.",
            "website_url": "https://icar.org.in", "email": "icar.help@icar.gov.in"
        },
        {
            "category": "email", "name": "Seed Division Support",
            "description": "Queries related to seed availability.",
            "website_url": "", "email": "seed-division@gov.in"
        },

        # 4. Crop Insurance & Subsidy
        {
            "category": "insurance", "name": "PM Fasal Bima Yojana (PMFBY)",
            "description": "Crop insurance scheme portal.",
            "website_url": "https://pmfby.gov.in", "helpline_number": "011-23382012"
        },
        {
            "category": "insurance", "name": "Agriculture Infra Fund",
            "description": "Financing facility for post-harvest management.",
            "website_url": "https://agriinfra.dac.gov.in", "helpline_number": ""
        },
        {
            "category": "insurance", "name": "Kisan Credit Card (KCC)",
            "description": "Information on credit access for farmers.",
            "website_url": "https://www.nabard.org", "helpline_number": "022-26539895"
        },
        {
            "category": "insurance", "name": "PMKSY (Irrigation)",
            "description": "Pradhan Mantri Krishi Sinchayee Yojana subsidy.",
            "website_url": "https://pmksy.gov.in", "helpline_number": ""
        },
        {
            "category": "insurance", "name": "Direct Benefit Transfer (DBT)",
            "description": "Subsidy transfer status check.",
            "website_url": "https://dbtbharat.gov.in", "helpline_number": ""
        },

        # 5. Weather & Advisory
        {
            "category": "advisory", "name": "IMD Mausam",
            "description": "Official weather forecasts by IMD.",
            "website_url": "https://mausam.imd.gov.in", "helpline_number": ""
        },
        {
            "category": "advisory", "name": "Meghdoot App",
            "description": "Agromet advisory service app.",
            "website_url": "https://play.google.com/store/apps/details?id=com.imd.mas", "helpline_number": ""
        },
        {
            "category": "advisory", "name": "Damini App (Lightning)",
            "description": "Lightning alert app for field safety.",
            "website_url": "", "helpline_number": ""
        },
        {
            "category": "advisory", "name": "ICAR Agromet Advisory",
            "description": "District-level agricultural advisories.",
            "website_url": "https://imdagrimet.gov.in", "helpline_number": ""
        },
        {
            "category": "advisory", "name": "State Agriculture Portal",
            "description": "State-specific weather and crop alerts.",
            "website_url": "https://farmer.gov.in", "helpline_number": ""
        },
    ]

    for data in resources:
        try:
             GovernmentResource.objects.create(**data)
             print(f"Created: {data['name']}")
        except Exception as e:
            print(f"Error creating {data['name']}: {e}")

populate()
