from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'product_type', 'description', 'price', 'unit', 'stock_quantity', 'reorder_level', 'image', 'image_url']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ['admin', 'agronomist', 'farmer']:
            messages.error(request, 'You do not have permission to add products.')
            return redirect('inventory:list')
        return super().dispatch(request, *args, **kwargs)
