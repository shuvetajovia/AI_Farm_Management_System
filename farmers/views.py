from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from .models import FarmerProfile, Land

class FarmerProfileView(LoginRequiredMixin, DetailView):
    model = FarmerProfile
    template_name = 'farmers/profile.html'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except:
            return redirect('farmers:profile_create')

    def get_object(self):
        return get_object_or_404(FarmerProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from soil.models import SoilData
        context['soil_reports_count'] = SoilData.objects.filter(land__farmer__user=self.request.user).count()
        return context

class FarmerProfileCreateView(LoginRequiredMixin, CreateView):
    model = FarmerProfile
    fields = ['phone', 'address', 'farm_size']
    template_name = 'farmers/profile_form.html'
    success_url = reverse_lazy('farmers:profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FarmerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = FarmerProfile
    fields = ['phone', 'address', 'farm_size']
    template_name = 'farmers/profile_form.html'
    success_url = reverse_lazy('farmers:profile')

    def get_object(self):
        return get_object_or_404(FarmerProfile, user=self.request.user)

class LandListView(LoginRequiredMixin, ListView):
    model = Land
    template_name = 'farmers/land_list.html'

    def get_queryset(self):
        return Land.objects.filter(farmer__user=self.request.user)

class LandCreateView(LoginRequiredMixin, CreateView):
    model = Land
    fields = ['name', 'area', 'soil_type', 'location', 'latitude', 'longitude']
    template_name = 'farmers/land_form.html'
    success_url = reverse_lazy('farmers:land_list')

    def form_valid(self, form):
        farmer_profile = get_object_or_404(FarmerProfile, user=self.request.user)
        form.instance.farmer = farmer_profile
        return super().form_valid(form)

class LandUpdateView(LoginRequiredMixin, UpdateView):
    model = Land
    fields = ['name', 'area', 'soil_type', 'location', 'latitude', 'longitude']
    template_name = 'farmers/land_form.html'
    success_url = reverse_lazy('farmers:land_list')

    def get_queryset(self):
        return Land.objects.filter(farmer__user=self.request.user)

from .models import GovernmentResource

def gov_help(request):
    # Lazy-populate if empty
    if GovernmentResource.objects.count() == 0:
        _populate_gov_resources()
    
    category = request.GET.get('category', 'all')
    resources = GovernmentResource.objects.filter(is_deleted=False)
    if category != 'all':
        resources = resources.filter(category=category)
    
    categories = GovernmentResource.objects.filter(is_deleted=False).values_list('category', flat=True).distinct()
    
    context = {
        'resources': resources,
        'categories': categories,
        'active_category': category,
    }
    return render(request, 'farmers/gov_help.html', context)


def _populate_gov_resources():
    resources = [
        {"category":"portal","name":"e-NAM (National Agriculture Market)","description":"Pan-India electronic trading portal for farm produce.","website_url":"https://www.enam.gov.in","helpline_number":"1800-270-0224"},
        {"category":"portal","name":"PM-KISAN Portal","description":"Direct income support portal for farmers.","website_url":"https://pmkisan.gov.in","helpline_number":"155261"},
        {"category":"portal","name":"Soil Health Card Portal","description":"Official portal for soil health tracking and reports.","website_url":"https://soilhealth.dac.gov.in","helpline_number":"011-23381385"},
        {"category":"portal","name":"MKisan Portal","description":"Unified mobile-based advisory services for farmers.","website_url":"https://mkisan.gov.in","helpline_number":"1800-180-1551"},
        {"category":"portal","name":"Jaivik Kheti Portal","description":"Dedicated portal for organic farming promotion.","website_url":"https://www.jaivikkheti.in","helpline_number":""},
        {"category":"helpline","name":"Kisan Call Center (KCC)","description":"National toll-free helpline for agricultural queries.","website_url":"https://dackkms.gov.in","helpline_number":"1800-180-1551"},
        {"category":"helpline","name":"Agriculture Emergency Helpline","description":"Disaster management control room for crop loss.","website_url":"","helpline_number":"1077"},
        {"category":"helpline","name":"Animal Husbandry Helpline","description":"Support for livestock diseases and care.","website_url":"","helpline_number":"1962"},
        {"category":"helpline","name":"Women Helpline (Kisan)","description":"Dedicated support line for women farmers.","website_url":"","helpline_number":"181"},
        {"category":"helpline","name":"Farm Distress Support","description":"Mental health support for distressed farmers.","website_url":"","helpline_number":"1800-599-0019"},
        {"category":"email","name":"Ministry of Agriculture Support","description":"General queries for the Ministry of Agriculture.","website_url":"https://agricoop.nic.in","email":"agri-help@gov.in"},
        {"category":"email","name":"PM-KISAN Helpdesk","description":"Email support for PM-KISAN payment issues.","website_url":"","email":"pmkisan-ict@gov.in"},
        {"category":"email","name":"e-NAM Technical Support","description":"Technical assistance for e-NAM trading portal.","website_url":"","email":"enam.helpdesk@gmail.com"},
        {"category":"email","name":"ICAR Info Desk","description":"Scientific queries and research information.","website_url":"https://icar.org.in","email":"icar.help@icar.gov.in"},
        {"category":"email","name":"Seed Division Support","description":"Queries related to seed availability and quality.","website_url":"","email":"seed-division@gov.in"},
        {"category":"insurance","name":"PM Fasal Bima Yojana (PMFBY)","description":"Crop insurance scheme for farmers.","website_url":"https://pmfby.gov.in","helpline_number":"011-23382012"},
        {"category":"insurance","name":"Agriculture Infra Fund","description":"Financing facility for post-harvest management.","website_url":"https://agriinfra.dac.gov.in","helpline_number":""},
        {"category":"insurance","name":"Kisan Credit Card (KCC)","description":"Credit access information for farmers via NABARD.","website_url":"https://www.nabard.org","helpline_number":"022-26539895"},
        {"category":"insurance","name":"PMKSY (Irrigation Subsidy)","description":"Pradhan Mantri Krishi Sinchayee Yojana.","website_url":"https://pmksy.gov.in","helpline_number":""},
        {"category":"insurance","name":"Direct Benefit Transfer (DBT)","description":"Check subsidy transfer status for farmers.","website_url":"https://dbtbharat.gov.in","helpline_number":""},
        {"category":"advisory","name":"IMD Mausam","description":"Official weather forecasts by India Meteorological Dept.","website_url":"https://mausam.imd.gov.in","helpline_number":""},
        {"category":"advisory","name":"Meghdoot App","description":"Agromet advisory service for farmers.","website_url":"https://play.google.com/store/apps/details?id=com.imd.mas","helpline_number":""},
        {"category":"advisory","name":"Damini App (Lightning)","description":"Lightning alert app for field safety.","website_url":"","helpline_number":""},
        {"category":"advisory","name":"ICAR Agromet Advisory","description":"District-level agricultural weather advisories.","website_url":"https://imdagrimet.gov.in","helpline_number":""},
        {"category":"advisory","name":"State Agriculture Portal","description":"State-specific weather and crop alerts.","website_url":"https://farmer.gov.in","helpline_number":""},
    ]
    for r in resources:
        GovernmentResource.objects.get_or_create(name=r['name'], defaults=r)
