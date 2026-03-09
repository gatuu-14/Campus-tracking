from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # =====================
    # Authentication
    # =====================
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),

    # =====================
    # Dashboard (Main Page)
    # =====================
    path('', views.dashboard, name='dashboard'),

    # =====================
    # Asset CRUD
    # =====================
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/import/', views.import_assets, name='import_assets'),

    # =====================
    # Asset Movements CRUD
    # =====================
    path('movements/', views.movement_list, name='movement_list'),
    path('movements/add/', views.add_movement, name='add_movement'),

    # =====================
    # Asset Maintenance CRUD
    # =====================
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),

    # =====================
    # Reports
    # =====================
    path('reports/', views.reports, name='reports'),

]
 
