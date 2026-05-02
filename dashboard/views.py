from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from farmers.models import FarmerProfile
from orders.models import Order
from inventory.models import Product

from farmers.models import FarmerProfile, Land
from soil.models import SoilData
from orders.models import Order
from crops.models import Crop
from inventory.models import Product

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_home(request):
    profile = FarmerProfile.objects.filter(user=request.user, is_deleted=False).first()
    
    active_farms = Land.objects.filter(farmer=profile, is_deleted=False).count() if profile else 0
    soil_records = SoilData.objects.filter(land__farmer=profile, is_deleted=False).count() if profile else 0
    pending_orders = Order.objects.filter(farmer=request.user, is_deleted=False, status='pending').count()
    crops_count = Crop.objects.filter(is_deleted=False).count()
    featured_products = Product.objects.filter(is_deleted=False)[:4]
    
    context = {
        'active_farms': active_farms,
        'soil_records': soil_records,
        'pending_orders': pending_orders,
        'crops_count': crops_count,
        'featured_products': featured_products,
        'profile': profile,
    }
    return render(request, 'dashboard/home.html', context)

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role in ['admin', 'agronomist']:
            context['farmer_count'] = FarmerProfile.objects.count()
            context['order_count'] = Order.objects.count()
            context['total_sales'] = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            context['low_stock_products'] = Product.objects.filter(stock_quantity__lte=models.F('reorder_level'))
        return context
