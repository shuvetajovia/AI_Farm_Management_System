from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    
    # Farmers
    path('farmers/', views.FarmerListView.as_view(), name='farmer_list'),
    path('farmers/<int:pk>/', views.FarmerDetailView.as_view(), name='farmer_detail'),
    path('farmers/<int:pk>/delete/', views.FarmerSoftDeleteView.as_view(), name='farmer_delete'),
    path('farmers/<int:pk>/restore/', views.FarmerRestoreView.as_view(), name='farmer_restore'),
    path('users/<int:pk>/role/', views.UserRoleUpdateView.as_view(), name='role_update'),

    
    # Lands
    path('lands/', views.LandListView.as_view(), name='land_list'),
    path('lands/<int:pk>/delete/', views.LandSoftDeleteView.as_view(), name='land_delete'),
    path('lands/<int:pk>/restore/', views.LandRestoreView.as_view(), name='land_restore'),
    
    # Soil
    path('soil/', views.SoilListView.as_view(), name='soil_list'),
    path('soil/<int:pk>/delete/', views.SoilSoftDeleteView.as_view(), name='soil_delete'),
    path('soil/<int:pk>/restore/', views.SoilRestoreView.as_view(), name='soil_restore'),
    
    # Inventory (Products)
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductSoftDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/restore/', views.ProductRestoreView.as_view(), name='product_restore'),
    
    # Orders
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderSoftDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/restore/', views.OrderRestoreView.as_view(), name='order_restore'),

    # Crops
    path('crops/', views.CropListView.as_view(), name='crop_list'),
    path('crops/create/', views.CropCreateView.as_view(), name='crop_create'),
    path('crops/<int:pk>/delete/', views.CropSoftDeleteView.as_view(), name='crop_delete'),
    
    # Logs & Export
    path('logs/', views.AdminLogListView.as_view(), name='log_list'),
    path('export/<str:model_type>/', views.ExportDataView.as_view(), name='export_data'),
]
