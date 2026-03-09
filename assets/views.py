from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Asset, Department, AssetCategory, AssetMovement, MaintenanceRecord
from .forms import AssetForm, MovementForm, MaintenanceForm, AssetImportForm
import csv
import json

# -------------------------------
# Login View
# -------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'assets/login.html')

# ===============================
# Logout View
# ===============================
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# ===============================
# Dashboard (MAIN PAGE)
# ===============================
@login_required
def dashboard(request):
    total_assets = Asset.objects.count()
    assets_in_use = Asset.objects.filter(status="In Use").count()
    assets_under_maintenance = Asset.objects.filter(status="Under Maintenance").count()
    department_count = Department.objects.count()

    # --- Assets by Condition --- 
    assets_by_condition = ( 
        Asset.objects.values('condition') 
        .annotate(total=Count('id')) 
        .order_by('condition') ) 
    condition_labels = [item['condition'] for item in assets_by_condition] 
    condition_data = [item['total'] for item in assets_by_condition]

    # --- Assets by Category --- 
    assets_by_category = ( 
        Asset.objects.values('category__name') 
        .annotate(total=Count('id')) 
        .order_by('category__name') ) 
    category_labels = [item['category__name'] or "Uncategorized" 
    for item in assets_by_category] 
    category_data = [item['total'] for item in assets_by_category] 
    if not category_labels: 
        category_labels = ['No Categories'] 
        category_data = [0]

    # --- Department Table Data  ---
    departments_with_assets = Department.objects.annotate(
        asset_count=Count('asset')
    ).order_by('-asset_count')
    
    for dept in departments_with_assets:
        if total_assets > 0:
            dept.percentage = round((dept.asset_count / total_assets) * 100, 1)
        else:
            dept.percentage = 0

    context = {
        'total_assets': total_assets,
        'assets_in_use': assets_in_use,
        'assets_under_maintenance': assets_under_maintenance,
        'condition_labels': json.dumps(condition_labels),
        'condition_data': json.dumps(condition_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'department_count': department_count,
        'departments_with_assets': departments_with_assets,  
    }

    return render(request, 'assets/dashboard.html', context)


# ===============================
# Asset CRUD 
# ===============================
@login_required
def asset_list(request):
    query = request.GET.get('q', '')
    assets = Asset.objects.select_related('department', 'category').all()

    if query:
        assets = assets.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(department__name__icontains=query)
        )

    return render(request, 'assets/asset_list.html', {'assets': assets, 'query': query})
@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()

    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Add Asset'})

# ===============================
# Asset Movements
# ===============================
@login_required
def movement_list(request):
    movements = AssetMovement.objects.select_related(
        'asset', 'from_department', 'to_department'
    ).order_by('-date_moved')

    return render(request, 'assets/movement_list.html', {'movements': movements})


@login_required
def add_movement(request):
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():

            asset = form.cleaned_data.get('asset')
            category = form.cleaned_data.get('category')

            # Prevent both selected
            if asset and category:
                messages.error(request, "Select either an asset or a category.")
                return render(request, 'assets/movement_form.html', {'form': form})

            # Category movement (batch)
            if category and not asset:
                assets = Asset.objects.filter(category=category)
                for a in assets:
                    AssetMovement.objects.create(
                        asset=a,
                        from_department=a.department,
                        to_department=form.cleaned_data.get('to_department'),
                        moved_by=request.user,
                        remarks=form.cleaned_data.get('remarks')
                    )
                return redirect('movement_list')

            # Single asset movement
            movement = form.save(commit=False)
            movement.moved_by = request.user
            movement.save()

            return redirect('movement_list')
    else:
        form = MovementForm()

    return render(request, 'assets/movement_form.html', {
        'form': form,
        'title': 'Record Movement'
    })


# ===============================
# Maintenance
# ===============================
@login_required
def maintenance_list(request):
    records = MaintenanceRecord.objects.select_related('asset').order_by('-maintenance_date')
    return render(request, 'assets/maintenance_list.html', {'records': records})


@login_required
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()

    return render(request, 'assets/maintenance_form.html', {
        'form': form,
        'title': 'Add Maintenance Record'
    })


# ===============================
# Reports
# ===============================
@login_required
def reports(request):
    # Annotate each asset with maintenance and movement counts
    assets = Asset.objects.annotate(
        maintenance_count=Count('maintenancerecord'),
        movement_count=Count('assetmovement')
    ).select_related('category', 'department')

    # Summary stats
    total_assets = assets.count()
    maintenance_count = MaintenanceRecord.objects.count()
    movement_count = AssetMovement.objects.count()

    # Assets by category and department (For the summary cards)
    assets_by_category = assets.values('category__name').annotate(count=Count('id'))
    assets_by_department = assets.values('department__name').annotate(count=Count('id'))

    context = {
        'assets': assets,
        'total_assets': total_assets,
        'maintenance_count': maintenance_count,
        'movement_count': movement_count,
        'assets_by_category': assets_by_category,
        'assets_by_department': assets_by_department,
    }
    return render(request, 'assets/reports.html', context)



# ===============================
# CSV Import
# ===============================
@login_required
def import_assets(request):
    if request.method == "POST":
        form = AssetImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded)

            for row in reader:
                category, _ = AssetCategory.objects.get_or_create(name=row['category'])
                department, _ = Department.objects.get_or_create(name=row['department'])

                Asset.objects.create(
                    name=row['name'],
                    category=category,
                    serial_number=row['serial_number'],
                    department=department,
                    purchase_date=row['purchase_date'],
                    status=row['status'],
                )

            return redirect('asset_list')
    else:
        form = AssetImportForm()

    return render(request, 'assets/import_assets.html', {'form': form})
