from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendations_home, name='home'),
    path('generate/', views.GenerateRecommendationsView.as_view(), name='generate'),
    path('fertilizer/', views.FertilizerRecommendationListView.as_view(), name='fertilizer_list'),
    path('crop/', views.CropRecommendationListView.as_view(), name='crop_list'),
    path('report/<int:land_id>/', views.SoilHealthReportView.as_view(), name='soil_report'),
    path('report/<int:land_id>/pdf/', views.DownloadSoilReportPDFView.as_view(), name='soil_report_pdf'),
]