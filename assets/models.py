from django.db import models
from django.contrib.auth.models import User

# Department model
class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    head_of_department = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  


# Asset Category
class AssetCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Asset Categories"


# Main Asset model
class Asset(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Disposed', 'Disposed'),
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField()
    condition = models.CharField(max_length=50, default="Good")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Available')
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    current_user = models.CharField(max_length=100, blank=True, null=True)
    last_checked_out = models.DateTimeField(blank=True, null=True)
    expected_return_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        ordering = ['-date_added']  


# Track movement of assets between departments
class AssetMovement(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    from_department = models.ForeignKey(Department, related_name='moved_from', on_delete=models.SET_NULL, null=True)
    to_department = models.ForeignKey(Department, related_name='moved_to', on_delete=models.SET_NULL, null=True)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_moved = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    # Optional: store category for batch movement 
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.asset.name} moved to {self.to_department}"

    class Meta:
        ordering = ['-date_moved']

        unique_together = ('asset', 'from_department', 'to_department', 'date_moved')

    # Auto-update Asset when movement is saved
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.to_department:
            self.asset.department = self.to_department
            self.asset.save()


# Track maintenance records
class MaintenanceRecord(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    issue_reported = models.TextField()
    maintenance_date = models.DateField()
    performed_by = models.CharField(max_length=100)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Maintenance for {self.asset.name} on {self.maintenance_date}"

    class Meta:
        ordering = ['-maintenance_date']
