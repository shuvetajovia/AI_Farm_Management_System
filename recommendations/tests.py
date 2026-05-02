from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from farmers.models import FarmerProfile, Land
from soil.models import SoilData
from crops.models import Crop
from decimal import Decimal
import datetime

User = get_user_model()

class SoilReportTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testfarmer', password='password123')
        self.client = Client()
        self.client.login(username='testfarmer', password='password123')

        # Get profile (created by signal) or create if not exists
        self.profile, _ = FarmerProfile.objects.get_or_create(user=self.user)
        self.profile.phone = '1234567890'
        self.profile.save()

        # Create Land
        self.land = Land.objects.create(
            farmer=self.profile,
            name="Test Field",
            area=Decimal('10.00'),
            soil_type="Loamy",
            location="Test Location"
        )

        # Create Crop
        self.crop = Crop.objects.create(
            name="Wheat",
            nitrogen_requirement=Decimal('100.00'),
            phosphorus_requirement=Decimal('50.00'),
            potassium_requirement=Decimal('40.00'),
            optimal_ph_min=Decimal('6.0'),
            optimal_ph_max=Decimal('7.0'),
            season='rabi'
        )

        # Create SoilData
        self.soil_data = SoilData.objects.create(
            land=self.land,
            date_tested=datetime.date.today(),
            ph_level=Decimal('6.5'),
            nitrogen=Decimal('80.00'),
            phosphorus=Decimal('20.00'),
            potassium=Decimal('30.00'),
            organic_carbon=Decimal('0.60'),
            moisture=Decimal('25.00')
        )

    def test_soil_report_view_status_code(self):
        url = reverse('recommendations:soil_report', kwargs={'land_id': self.land.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_soil_report_content(self):
        url = reverse('recommendations:soil_report', kwargs={'land_id': self.land.id})
        response = self.client.get(url)
        self.assertContains(response, "Soil Health Analysis Report")
        self.assertContains(response, "Test Field")
        self.assertContains(response, "Loamy")
        self.assertContains(response, "0.60") # Organic Carbon
