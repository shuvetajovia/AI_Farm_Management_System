from django.urls import path
from . import views

app_name = 'farmers'

urlpatterns = [
    path('', views.LandListView.as_view(), name='land_list'),
    path('land/add/', views.LandCreateView.as_view(), name='land_create'),
    path('land/<int:pk>/edit/', views.LandUpdateView.as_view(), name='land_update'),
    path('land/<int:pk>/delete/', views.LandListView.as_view(), name='land_delete'),
    path('profile/', views.FarmerProfileView.as_view(), name='profile'),
    path('profile/edit/', views.FarmerProfileUpdateView.as_view(), name='profile_edit'),
    path('gov-help/', views.gov_help, name='gov_help'),
]