from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # =====================
    # Authentication Routes
    # =====================
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),

    # =====================
    # Core Pages
    # =====================
    path('', views.home, name='home'),  # Home after login
    path('dashboard/', views.dashboard, name='dashboard'),  # Analytics dashboard

    # =====================
    # Asset Views
    # =====================
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/<int:id>/', views.asset_detail, name='asset_detail'),
    path('assets/edit/<int:id>/', views.edit_asset, name='edit_asset'),
    path('assets/delete/<int:id>/', views.delete_asset, name='delete_asset'),
    path('assets/<int:asset_id>/checkout/', views.checkout_asset, name='checkout_asset'),
    path('assets/<int:asset_id>/return/', views.return_asset, name='return_asset'),
    path('assets/import/', views.import_assets, name='import_assets'),

    # =====================
    # Asset Movement Views
    # =====================
    path('movements/', views.movement_list, name='movement_list'),
    path('movements/add/', views.add_movement, name='add_movement'),
    path('movements/<int:id>/edit/', views.edit_movement, name='edit_movement'),
    path('movements/<int:id>/delete/', views.delete_movement, name='delete_movement'),

    # =====================
    # Maintenance Views
    # =====================
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/<int:id>/edit/', views.edit_maintenance, name='edit_maintenance'),
    path('maintenance/<int:id>/delete/', views.delete_maintenance, name='delete_maintenance'),

    # =====================
    # Reports
    # =====================
    path('reports/', views.reports, name='reports'),
]
