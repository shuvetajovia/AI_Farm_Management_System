from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.CropListView.as_view(), name='list'),
    path('<int:pk>/', views.CropDetailView.as_view(), name='detail'),
]