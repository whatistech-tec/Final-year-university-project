from django.db import models

from django.utils import timezone


# Base model for common fields
class BaseModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

# Vehicle Details
class VehicleDetail(BaseModel):
    vehicle_image = models.ImageField(null=True, blank=True, upload_to='vehicles/')
    plate_number = models.CharField(max_length=200, default='')
    vehicle_name = models.CharField(max_length=250)
    vehicle_color = models.CharField(max_length=200, default='')
    vehicle_category = models.CharField(max_length=200, default='')
    mileage = models.FloatField(default=0)
    speed = models.IntegerField(default=0)
    settings = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    location = models.CharField(max_length=50)
    hire_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    in_stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    
    
    
    
    def __str__(self):
        return f"{self.vehicle_name} ({self.plate_number})"

# Rented Vehicle
class RentedVehicle(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    company_branch = models.CharField(max_length=255, default='')
    car_model = models.CharField(max_length=200, default='')
    plate_number = models.CharField(max_length=200, default='')
    car_color = models.CharField(max_length=200, default='')
    hire_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='Success')
    
    def __str__(self):
        return f"Rental: {self.first_name} {self.last_name} - {self.plate_number}"

# User Information
class UsersInfo(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    is_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.username} (Admin: {self.is_admin})"

# Rental Stories
class Stories(BaseModel):
    story_image = models.ImageField(null=True, blank=True, upload_to='stories/')
    date = models.IntegerField(default=0)
    month = models.CharField(max_length=50)
    year = models.IntegerField(default=0)
    header = models.CharField(max_length=50)
    story = models.TextField()

    def __str__(self):
        return f"Story: {self.header} - {self.month} {self.year}"

# Payment Transaction
class Transaction(models.Model):
    name = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=300, default="")
    city = models.CharField(max_length=255, default='Nairobi')
    national_id = models.CharField(max_length=200, default='')
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    hire_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    vehicle_name = models.CharField(max_length=255, default='')
    vehicle_color = models.CharField(max_length=200, default='')
    plate_number =  models.CharField(max_length=200, default='')
    transactionCode =  models.CharField(max_length=200, default='')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rental: {self.name}"


