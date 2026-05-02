from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.urls import reverse_lazy
from django.forms import DateInput
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import SoilData
from farmers.models import Land
from recommendations.models import CropRecommendation, FertilizerRecommendation

from recommendations.views import GenerateRecommendationsView

class SoilReportPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        soil_data = get_object_or_404(SoilData, pk=pk)
        
        # Generate recommendations on the fly using the existing logic
        generator = GenerateRecommendationsView()
        
        # Get Crop Recommendations
        all_crop_recs = generator.generate_crop_recommendations(soil_data.land, soil_data)
        
        # Get Fertilizer Recommendations
        all_fert_recs = generator.generate_fertilizer_recommendations(soil_data.land, soil_data)

        context = {
            'object': soil_data,
            'crop_recs': all_crop_recs,
            'fert_recs': all_fert_recs,
        }

        template_path = 'soil/report_pdf.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Soil_Report_{soil_data.pk}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class SoilDataListView(LoginRequiredMixin, ListView):
    model = SoilData
    template_name = 'soil/soil_list.html'

    def get_queryset(self):
        return SoilData.objects.filter(land__farmer__user=self.request.user)

class SoilDataCreateView(LoginRequiredMixin, CreateView):
    model = SoilData
    fields = ['land', 'date_tested', 'ph_level', 'nitrogen', 'phosphorus', 'potassium', 'organic_carbon', 'moisture', 'notes']
    template_name = 'soil/soil_form.html'
    success_url = reverse_lazy('soil:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['land'].queryset = Land.objects.filter(farmer__user=self.request.user)
        form.fields['date_tested'].widget = DateInput(attrs={'type': 'date'})
        return form

    def get(self, request, *args, **kwargs):
        # Check if user has any lands
        if not Land.objects.filter(farmer__user=self.request.user).exists():
            from django.contrib import messages
            messages.warning(request, 'You need to add land details first before adding soil data. Please visit your profile to add lands.')
            return redirect('farmers:land_list')
        return super().get(request, *args, **kwargs)

class SoilDataDetailView(LoginRequiredMixin, DetailView):
    model = SoilData
    template_name = 'soil/soil_detail.html'

    def get_queryset(self):
        return SoilData.objects.filter(land__farmer__user=self.request.user)

class SoilDataUpdateView(LoginRequiredMixin, UpdateView):
    model = SoilData
    fields = ['land', 'date_tested', 'ph_level', 'nitrogen', 'phosphorus', 'potassium', 'organic_carbon', 'moisture', 'notes']
    template_name = 'soil/soil_form.html'
    success_url = reverse_lazy('soil:list')

    def get_queryset(self):
        return SoilData.objects.filter(land__farmer__user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['land'].queryset = Land.objects.filter(farmer__user=self.request.user)
        form.fields['date_tested'].widget = DateInput(attrs={'type': 'date'})
        return form
