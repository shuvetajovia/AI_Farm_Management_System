from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, View, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from django.http import HttpResponse
import csv

from .models import AdminLog
from .mixins import SuperAdminRequiredMixin, ManagerAdminRequiredMixin
from accounts.models import CustomUser
from farmers.models import FarmerProfile, Land
from crops.models import Crop
from orders.models import Order
from inventory.models import Product
from soil.models import SoilData

# --- LOGGING HELPER ---
def log_admin_action(user, action, model_name, object_repr, details=""):
    AdminLog.objects.create(
        admin_user=user,
        action=action,
        model_name=model_name,
        object_repr=object_repr,
        details=details
    )

# --- DASHBOARD ---
class AdminDashboardView(ManagerAdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Stats
        context['total_farmers'] = FarmerProfile.objects.filter(is_deleted=False).count()
        context['active_lands'] = Land.objects.filter(is_deleted=False).count()
        context['total_orders'] = Order.objects.filter(is_deleted=False).count()
        context['total_revenue'] = Order.objects.filter(is_deleted=False).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Recent Logs (last 10)
        context['recent_logs'] = AdminLog.objects.all()[:10]
        return context

# --- FARMER MANAGEMENT ---
class FarmerListView(ManagerAdminRequiredMixin, ListView):
    model = FarmerProfile
    template_name = 'custom_admin/farmer_list.html'
    context_object_name = 'farmers'
    
    def get_queryset(self):
        return FarmerProfile.objects.all().select_related('user').order_by('-user__date_joined')

class FarmerDetailView(ManagerAdminRequiredMixin, DetailView):
    model = FarmerProfile
    template_name = 'custom_admin/farmer_detail.html'
    context_object_name = 'farmer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lands'] = self.object.lands.filter(is_deleted=False)
        context['orders'] = Order.objects.filter(farmer=self.object.user).order_by('-order_date')
        return context

class FarmerSoftDeleteView(ManagerAdminRequiredMixin, View):
    def post(self, request, pk):
        farmer = get_object_or_404(FarmerProfile, pk=pk)
        farmer.is_deleted = True
        farmer.save()
        farmer.user.is_active = False
        farmer.user.save()
        
        log_admin_action(request.user, 'DELETE', 'FarmerProfile', str(farmer), "Soft deleted farmer account")
        messages.success(request, f"Farmer {farmer} deactivated.")
        return redirect('custom_admin:farmer_list')

class FarmerRestoreView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        farmer = get_object_or_404(FarmerProfile, pk=pk)
        farmer.is_deleted = False
        farmer.save()
        farmer.user.is_active = True
        farmer.user.save()
        
        log_admin_action(request.user, 'RESTORE', 'FarmerProfile', str(farmer), "Restored farmer account")
        messages.success(request, f"Farmer {farmer} restored.")
        return redirect('custom_admin:farmer_list')

# --- LAND MANAGEMENT ---
class LandListView(ManagerAdminRequiredMixin, ListView):
    model = Land
    template_name = 'custom_admin/land_list.html'
    context_object_name = 'lands'

    def get_queryset(self):
        return Land.objects.all().select_related('farmer', 'farmer__user')

class LandSoftDeleteView(ManagerAdminRequiredMixin, View):
    def post(self, request, pk):
        land = get_object_or_404(Land, pk=pk)
        land.is_deleted = True
        land.save()
        log_admin_action(request.user, 'DELETE', 'Land', str(land))
        messages.success(request, "Land marked as deleted.")
        return redirect('custom_admin:land_list')

class LandRestoreView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        land = get_object_or_404(Land, pk=pk)
        land.is_deleted = False
        land.save()
        log_admin_action(request.user, 'RESTORE', 'Land', str(land))
        messages.success(request, "Land restored.")
        return redirect('custom_admin:land_list')

# --- SOIL MANAGEMENT ---
class SoilListView(ManagerAdminRequiredMixin, ListView):
    model = SoilData
    template_name = 'custom_admin/soil_list.html'
    context_object_name = 'soil_reports'

    def get_queryset(self):
        return SoilData.objects.all().select_related('land', 'land__farmer__user')

class SoilSoftDeleteView(ManagerAdminRequiredMixin, View):
    def post(self, request, pk):
        soil = get_object_or_404(SoilData, pk=pk)
        soil.is_deleted = True
        soil.save()
        log_admin_action(request.user, 'DELETE', 'SoilData', str(soil))
        messages.success(request, "Soil report deleted.")
        return redirect('custom_admin:soil_list')

class SoilRestoreView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        soil = get_object_or_404(SoilData, pk=pk)
        soil.is_deleted = False
        soil.save()
        log_admin_action(request.user, 'RESTORE', 'SoilData', str(soil))
        messages.success(request, "Soil report restored.")
        return redirect('custom_admin:soil_list')

# --- INVENTORY & PRODUCTS ---
class ProductListView(ManagerAdminRequiredMixin, ListView):
    model = Product
    template_name = 'custom_admin/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.all()

class ProductCreateView(ManagerAdminRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'product_type', 'description', 'price', 'unit', 'stock_quantity', 'reorder_level', 'image', 'image_url']
    template_name = 'custom_admin/product_form.html'
    success_url = reverse_lazy('custom_admin:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_admin_action(self.request.user, 'CREATE', 'Product', str(self.object))
        return response

class ProductUpdateView(ManagerAdminRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'product_type', 'description', 'price', 'unit', 'stock_quantity', 'reorder_level', 'image', 'image_url']
    template_name = 'custom_admin/product_form.html'
    success_url = reverse_lazy('custom_admin:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_admin_action(self.request.user, 'UPDATE', 'Product', str(self.object))
        return response

class ProductSoftDeleteView(ManagerAdminRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_deleted = True
        product.save()
        log_admin_action(request.user, 'DELETE', 'Product', str(product))
        messages.success(request, "Product deactivated.")
        return redirect('custom_admin:product_list')

class ProductRestoreView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_deleted = False
        product.save()
        log_admin_action(request.user, 'RESTORE', 'Product', str(product))
        messages.success(request, "Product restored.")
        return redirect('custom_admin:product_list')

# --- CROP MANAGEMENT ---
class CropListView(ManagerAdminRequiredMixin, ListView):
    model = Crop
    template_name = 'custom_admin/crop_list.html'
    queryset = Crop.objects.all()

class CropCreateView(ManagerAdminRequiredMixin, CreateView):
    model = Crop
    fields = ['name', 'season', 'nitrogen_requirement', 'phosphorus_requirement', 'potassium_requirement', 'optimal_ph_min', 'optimal_ph_max', 'description']
    template_name = 'custom_admin/crop_form.html'
    success_url = reverse_lazy('custom_admin:crop_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_admin_action(self.request.user, 'CREATE', 'Crop', str(self.object))
        return response

class CropSoftDeleteView(ManagerAdminRequiredMixin, View):
    def post(self, request, pk):
        crop = get_object_or_404(Crop, pk=pk)
        crop.is_deleted = True
        crop.save()
        log_admin_action(request.user, 'DELETE', 'Crop', str(crop))
        messages.success(request, "Crop deleted.")
        return redirect('custom_admin:crop_list')

# --- ORDER MANAGEMENT ---
class OrderListView(ManagerAdminRequiredMixin, ListView):
    model = Order
    template_name = 'custom_admin/order_list.html'
    context_object_name = 'orders'
    ordering = ['-order_date']

class OrderUpdateView(ManagerAdminRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'custom_admin/order_form.html'
    success_url = reverse_lazy('custom_admin:order_list')

    def form_valid(self, form):
        if form.has_changed():
            log_admin_action(self.request.user, 'UPDATE', 'Order', str(self.object), f"Status changed to {self.object.status}")
        return super().form_valid(form)

class OrderSoftDeleteView(ManagerAdminRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.is_deleted = True
        order.save()
        log_admin_action(request.user, 'DELETE', 'Order', str(order))
        messages.success(request, "Order deleted.")
        return redirect('custom_admin:order_list')

class OrderRestoreView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.is_deleted = False
        order.save()
        log_admin_action(request.user, 'RESTORE', 'Order', str(order))
        messages.success(request, "Order restored.")
        return redirect('custom_admin:order_list')

# --- EXPORT ---
class ExportDataView(SuperAdminRequiredMixin, View):
    def get(self, request, model_type):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_type}_export.csv"'
        
        writer = csv.writer(response)
        
        if model_type == 'farmers':
            writer.writerow(['ID', 'Username', 'Phone', 'Farm Size', 'Is Active'])
            for f in FarmerProfile.objects.all():
                writer.writerow([f.id, f.user.username, f.phone, f.farm_size, f.user.is_active])
                
        elif model_type == 'orders':
            writer.writerow(['ID', 'Farmer', 'Amount', 'Date', 'Status'])
            for o in Order.objects.all():
                writer.writerow([o.id, o.farmer.username, o.total_amount, o.order_date, o.status])

        elif model_type == 'products':
            writer.writerow(['ID', 'Name', 'Type', 'Price', 'Stock'])
            for p in Product.objects.all():
                writer.writerow([p.id, p.name, p.product_type, p.price, p.stock_quantity])

        elif model_type == 'crops':
            writer.writerow(['ID', 'Name', 'Season', 'Type'])
            for c in Crop.objects.all():
                writer.writerow([c.id, c.name, c.season])

        log_admin_action(request.user, 'EXPORT', model_type, 'CSV Export')
        return response

# --- LOGS ---
class AdminLogListView(SuperAdminRequiredMixin, ListView):
    model = AdminLog
    template_name = 'custom_admin/log_list.html'
    paginate_by = 50
    ordering = ['-timestamp']

# --- USER ROLE MANAGEMENT ---
from .forms import AdminUserRoleForm

class UserRoleUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = AdminUserRoleForm
    template_name = 'custom_admin/user_role_form.html'
    success_url = reverse_lazy('custom_admin:farmer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_admin_action(self.request.user, 'UPDATE_ROLE', 'User', self.object.username, f"Role changed to {self.object.role}")
        messages.success(self.request, f"Role for {self.object.username} updated to {self.object.role}.")
        return response

