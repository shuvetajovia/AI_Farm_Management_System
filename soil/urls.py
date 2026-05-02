from django.urls import path
from . import views

app_name = 'soil'

urlpatterns = [
    path('', views.SoilDataListView.as_view(), name='list'),
    path('create/', views.SoilDataCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SoilDataDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.SoilDataUpdateView.as_view(), name='update'),
    path('<int:pk>/report/', views.SoilReportPDFView.as_view(), name='report'),
]