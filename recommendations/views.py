from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib import messages
from django.db.models import Q
from .models import FertilizerRecommendation, CropRecommendation
from farmers.models import Land
from soil.models import SoilData
from crops.models import Crop
from datetime import date
from decimal import Decimal

class SoilHealthReportView(LoginRequiredMixin, TemplateView):
    template_name = 'recommendations/soil_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        land_id = self.kwargs.get('land_id')
        
        # Get land and ensure it belongs to the user
        land = get_object_or_404(Land, id=land_id, farmer__user=self.request.user)
        
        # Get latest soil data
        soil_data = SoilData.objects.filter(land=land).order_by('-date_tested').first()
        
        if not soil_data:
            messages.warning(self.request, "No soil data found for this land. Cannot generate report.")
            # In a real scenario, might redirect, but for report generation we might want to show empty state or handle differently
            # For now, we will pass None and handle in template if needed, or redirect in get()
        
        # We can reuse the logic from GenerateRecommendationsView or extract it to a service.
        # For expediency, we will instantiate the view helper or duplicate logic slightly to pass context.
        # A cleaner way is to make the logic static or mixin. 
        # I will borrow the logic directly here to ensure the report gets the exact same data.
        
        generator = GenerateRecommendationsView()
        # Note: self.request is available
        
        fertilizer_recs = []
        crop_recs = []
        
        if soil_data:
            fertilizer_recs = generator.generate_fertilizer_recommendations(land, soil_data, limit=None)
            crop_recs = generator.generate_crop_recommendations(land, soil_data, limit=None)

        context.update({
            'land': land,
            'soil_data': soil_data,
            'fertilizer_recommendations': fertilizer_recs,
            'crop_recommendations': crop_recs,
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context['soil_data']:
             messages.error(request, 'No soil data found for this land.')
             return redirect('recommendations:home')
        return self.render_to_response(context)


from farmers.models import FarmerProfile, Land

def recommendations_home(request):
    profile = FarmerProfile.objects.filter(user=request.user, is_deleted=False).first()
    lands = Land.objects.filter(farmer=profile, is_deleted=False) if profile else Land.objects.none()
    
    crop_recommendations = []
    fertilizer_recommendations = []
    
    if profile:
        from recommendations.models import CropRecommendation, FertilizerRecommendation
        crop_recommendations = CropRecommendation.objects.filter(
            land__farmer=profile
        ).select_related('recommended_crop', 'land').order_by('-date_recommended')[:10]
        
        fertilizer_recommendations = FertilizerRecommendation.objects.filter(
            land__farmer=profile
        ).select_related('crop', 'land').order_by('-date_recommended')[:10]
    
    context = {
        'lands': lands,
        'profile': profile,
        'crop_recommendations': crop_recommendations,
        'fertilizer_recommendations': fertilizer_recommendations,
    }
    return render(request, 'recommendations/home.html', context)

class GenerateRecommendationsView(LoginRequiredMixin, TemplateView):
    template_name = 'recommendations/results.html'

    def get(self, request, *args, **kwargs):
        land_id = request.GET.get('land')
        if not land_id:
            messages.error(request, 'Please select a land parcel.')
            return redirect('recommendations:home')

        try:
            land = Land.objects.get(id=land_id, farmer__user=request.user)
        except Land.DoesNotExist:
            messages.error(request, 'Land not found.')
            return redirect('recommendations:home')

        # Get latest soil data for the land
        soil_data = SoilData.objects.filter(land=land).order_by('-date_tested', '-id').first()
        if not soil_data:
            messages.warning(request, f'No soil data found for {land.name}. Please add soil test data first.')
            return redirect('farmers:land_list')

        # Generate recommendations
        fertilizer_recs = self.generate_fertilizer_recommendations(land, soil_data)
        crop_recs = self.generate_crop_recommendations(land, soil_data)

        # Save recommendations to database for future reference
        from recommendations.models import CropRecommendation, FertilizerRecommendation
        
        # Wipe old recommendations for this specific land to keep it current
        CropRecommendation.objects.filter(land=land).delete()
        FertilizerRecommendation.objects.filter(land=land).delete()
        
        # Save Top 10 crop matches
        for rec in crop_recs[:10]:
            CropRecommendation.objects.create(
                land=land,
                recommended_crop=rec['crop'],
                reason=rec['reason']
            )
            
        # Save Top 10 fertilizer recommendations
        for rec in fertilizer_recs[:10]:
            notes_str = "; ".join(rec.get('fertilizer_suggestions', []))
            if rec.get('notes'):
                notes_str += f" | {rec['notes']}"
                
            FertilizerRecommendation.objects.create(
                land=land,
                crop=rec['crop'],
                nitrogen_recommended=rec['nitrogen_recommended'],
                phosphorus_recommended=rec['phosphorus_recommended'],
                potassium_recommended=rec['potassium_recommended'],
                notes=notes_str
            )

        context = {
            'land': land,
            'soil_data': soil_data,
            'fertilizer_recommendations': fertilizer_recs,
            'crop_recommendations': crop_recs,
        }

        return self.render_to_response(context)

    def generate_fertilizer_recommendations(self, land, soil_data, limit=10):
        """Generate fertilizer recommendations based on soil data and crop requirements with AI-like analysis"""
        recommendations = []

        # Get all crops
        crops = Crop.objects.all()

        for crop in crops:
            # Calculate deficiencies with more sophisticated analysis
            n_current = soil_data.nitrogen
            p_current = soil_data.phosphorus
            k_current = soil_data.potassium

            n_required = crop.nitrogen_requirement
            p_required = crop.phosphorus_requirement
            k_required = crop.potassium_requirement

            # Calculate deficiencies (ensure non-negative)
            n_deficiency = max(Decimal('0'), n_required - n_current)
            p_deficiency = max(Decimal('0'), p_required - p_current)
            k_deficiency = max(Decimal('0'), k_required - k_current)

            # Determine fertilizer type recommendations
            fertilizer_suggestions = []
            
            # Logic: If limit is None (Report Mode), include everything even if deficiency is low
            # If limit is set (Web Mode), apply threshold
            
            total_deficiency = n_deficiency + p_deficiency + k_deficiency
            threshold = (n_required + p_required + k_required) * Decimal('0.1')
            
            is_deficient = total_deficiency > threshold
            
            if is_deficient or limit is None:
                # Calculate recommended amounts with intelligent buffering
                # Use different buffers based on deficiency severity
                if n_deficiency > n_required * Decimal('0.5'):  # Severe deficiency
                    n_buffer = Decimal('1.3')
                elif n_deficiency > n_required * Decimal('0.2'):  # Moderate deficiency
                    n_buffer = Decimal('1.2')
                else:  # Mild deficiency
                    n_buffer = Decimal('1.1')

                if p_deficiency > p_required * Decimal('0.5'):
                    p_buffer = Decimal('1.3')
                elif p_deficiency > p_required * Decimal('0.2'):
                    p_buffer = Decimal('1.2')
                else:
                    p_buffer = Decimal('1.1')

                if k_deficiency > k_required * Decimal('0.5'):
                    k_buffer = Decimal('1.3')
                elif k_deficiency > k_required * Decimal('0.2'):
                    k_buffer = Decimal('1.2')
                else:
                    k_buffer = Decimal('1.1')

                n_rec = n_deficiency * n_buffer
                p_rec = p_deficiency * p_buffer
                k_rec = k_deficiency * k_buffer

                if n_rec > 0:
                    fertilizer_suggestions.append(f"Urea or Ammonium Sulphate for Nitrogen ({n_rec:.1f} kg/acre)")
                if p_rec > 0:
                    fertilizer_suggestions.append(f"Single Super Phosphate or DAP for Phosphorus ({p_rec:.1f} kg/acre)")
                if k_rec > 0:
                    fertilizer_suggestions.append(f"Muriate of Potash for Potassium ({k_rec:.1f} kg/acre)")
                
                if not fertilizer_suggestions and limit is None:
                     fertilizer_suggestions.append("Nutrient levels sufficient. No additional fertilizer required.")

                recommendations.append({
                    'crop': crop,
                    'crop_name': crop.name,
                    'nitrogen_recommended': round(n_rec, 2),
                    'phosphorus_recommended': round(p_rec, 2),
                    'potassium_recommended': round(k_rec, 2),
                    'fertilizer_suggestions': fertilizer_suggestions,
                    'notes': f"Soil Analysis: N={n_current}, P={p_current}, K={k_current} ppm. "
                           f"Crop Requirements: N={n_required}, P={p_required}, K={k_required} kg/acre. "
                           f"Deficiencies addressed with intelligent buffering based on severity."
                })

        # Sort by total fertilizer requirement (most needed first)
        recommendations.sort(key=lambda x: x['nitrogen_recommended'] + x['phosphorus_recommended'] + x['potassium_recommended'], reverse=True)
        if limit:
            return recommendations[:limit]
        return recommendations

    def calculate_crop_score(self, soil_data, crop):
        """
        Calculates a strict score (0-10) for a crop based on soil parameters.
        Returns: (score, suitability_label, reason_list)
        """
        score = Decimal('10.0')
        reasons = []
        caps = []  # Conditions that cap the maximum score

        # 1. Season Compatibility (Critical)
        current_month = date.today().month
        is_season_match = False
        
        if crop.season == 'kharif' and current_month in [6, 7, 8, 9, 10]: is_season_match = True
        elif crop.season == 'rabi' and current_month in [10, 11, 12, 1, 2, 3]: is_season_match = True
        elif crop.season == 'zaid' and current_month in [3, 4, 5, 6]: is_season_match = True
        
        if not is_season_match:
            return 0, "Not Suitable", [f"Wrong season. Current month does not match {crop.season} cycle."]

        # 2. pH Compatibility
        # Optimal range +/- 0.5 is Good, +/- 1.0 is Acceptable, else Penalty
        avg_optimal_ph = (crop.optimal_ph_min + crop.optimal_ph_max) / 2
        ph_diff = abs(soil_data.ph_level - avg_optimal_ph)
        
        if ph_diff > 1.5:
             caps.append(3) # Cap at 3 for severe pH mismatch
             reasons.append(f"Soil pH {soil_data.ph_level} is unsuitable for {crop.name} (Optimal: {crop.optimal_ph_min}-{crop.optimal_ph_max})")
             score -= 5
        elif ph_diff > 0.5:
             score -= 2
             reasons.append("pH is slightly off-optimal but acceptable.")

        # 3. Nutrient Sufficiency (N, P, K)
        # We calculate specific deficiency. Severe deficiency caps the score.
        def check_nutrient(current, required, name):
            if required == 0: return 0
            ratio = current / required
            if ratio < 0.3: # Less than 30% of required available
                return 2 # Severe penalty capability
            elif ratio < 0.6:
                return 1 # Moderate penalty
            return 0

        n_pen = check_nutrient(soil_data.nitrogen, crop.nitrogen_requirement, "Nitrogen")
        p_pen = check_nutrient(soil_data.phosphorus, crop.phosphorus_requirement, "Phosphorus")
        k_pen = check_nutrient(soil_data.potassium, crop.potassium_requirement, "Potassium")

        if n_pen == 2 or p_pen == 2 or k_pen == 2:
            caps.append(4)
            reasons.append("Severe nutrient deficiency detected (critical levels low).")
            score -= 4
        elif n_pen == 1 or p_pen == 1 or k_pen == 1:
            score -= 2
            reasons.append("Moderate nutrient deficiency - requires fertilization.")

        # 4. Moisture (Simplified)
        if soil_data.moisture < 20:
             score -= 1
             reasons.append("Low soil moisture.")

        # Apply Caps
        if caps:
            score = min(score, Decimal(min(caps)))

        # Finalize
        score = max(Decimal('0'), score)
        final_score = int(score)

        if final_score >= 8:
            label = "Suitable"
        elif final_score >= 5:
            label = "Conditionally Suitable"
        else:
            label = "Requires Intervention"

        return final_score, label, reasons

    def generate_crop_recommendations(self, land, soil_data, limit=20):
        """Generate crop recommendations using strict logic."""
        recommendations = []
        crops = Crop.objects.all()

        for crop in crops:
            score, suitability, reasons = self.calculate_crop_score(soil_data, crop)
            
            # Filter Safety Rule: Relaxed to show crops that need work (Score >= 3)
            # Only filter out absolutely impossible crops (Score < 3)
            if score < 3 and limit is not None:
                continue

            recommendations.append({
                'crop': crop,
                'score': score,
                'suitability': suitability,
                'reason': "; ".join(reasons) if reasons else "Good match for current conditions.",
                'estimated_yield': "Yield Estimate: Standard" # Placeholder
            })

        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        if limit:
            return recommendations[:limit]
        return recommendations

class FertilizerRecommendationListView(LoginRequiredMixin, ListView):
    model = FertilizerRecommendation
    template_name = 'recommendations/fertilizer_list.html'

    def get_queryset(self):
        return FertilizerRecommendation.objects.filter(land__farmer__user=self.request.user)

class CropRecommendationListView(LoginRequiredMixin, ListView):
    model = CropRecommendation
    template_name = 'recommendations/crop_list.html'

    def get_queryset(self):
        return CropRecommendation.objects.filter(land__farmer__user=self.request.user)

from .utils import render_to_pdf

class DownloadSoilReportPDFView(SoilHealthReportView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context['soil_data']:
             messages.error(request, 'No soil data found for this land.')
             return redirect('recommendations:home')
        
        # Render to PDF
        pdf = render_to_pdf('recommendations/soil_report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Soil_Report_{context['land'].name}_{date.today()}.pdf"
            content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Error Rendering PDF", status=400)
