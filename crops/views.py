from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Crop

class CropListView(LoginRequiredMixin, ListView):
    model = Crop
    template_name = 'crops/crop_list.html'

class CropDetailView(LoginRequiredMixin, DetailView):
    model = Crop
    template_name = 'crops/crop_detail.html'
