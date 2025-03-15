from django.db import models

class VehicleDetail(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    vehicle_image = models.ImageField(null=True, blank=True)
    plate_number = models.CharField(max_length=200, default='')
    vehicle_name = models.CharField(max_length=250)
    vehicle_color = models.CharField(max_length=200, default='')
    vehicle_category = models.CharField(max_length=200, default='')
    milage = models.FloatField(default=0)
    speed = models.IntegerField(default=0)
    settings = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    location = models.CharField(max_length=50)
    hire_amount = models.FloatField(default=0)
    in_stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.vehicle_name}"

    
class RentedVehicle(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    company_branch = models.CharField(max_length=255, default='')
    car_model = models.CharField(max_length=200, default='')
    plate_number = models.CharField(max_length=200, default='')
    car_color = models.CharField(max_length=200, default='')
    agent_name = models.CharField(max_length=200, default='')
    agent_number = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.first_name + "   " + self.last_name
    
class Stories(models.Model):
    story_image = models.ImageField(null=True, blank=True, upload_to='stories/')
    date = models.IntegerField(default=0)
    month = models.CharField(max_length=50)
    year = models.IntegerField(default=0)
    header = models.CharField(max_length=50)
    story = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.header}"
    
    
class UsersInfo(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=250)
    is_admin = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.username}"
    
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_id = models.CharField(max_length=100, unique=True)
    mpesa_code = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mpesa_code} - {self.amount} KES"



