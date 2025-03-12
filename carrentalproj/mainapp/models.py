from django.db import models


class VehicleDetail(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    vehicle_image = models.ImageField(null=True, blank=True)
    plate_number = models.CharField(max_length=200, default='')
    vehicle_name = models.CharField(max_length=250)
    vehicle_color = models.CharField(max_length=200, default='')
    vehicle_category = models.CharField(max_length=250)
    milage = models.FloatField(default=0)
    speed = models.IntegerField(default=0)
    settings = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    location = models.CharField(max_length=50)
    hire_amount = models.FloatField(default=0)
    
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


class MyCars(models.Model):
    car_image = models.ImageField(null=True, blank=True)
    hire_amount = models.FloatField(default=0)
    location = models.CharField(max_length=50)
    car_name = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.car_name}"
    
class MyVans(models.Model):
    car_image = models.ImageField(null=True, blank=True)
    hire_amount = models.FloatField(default=0)
    location = models.CharField(max_length=50)
    car_name = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.car_name}"
    
class MySuvs(models.Model):
    car_image = models.ImageField(null=True, blank=True)
    hire_amount = models.FloatField(default=0)
    location = models.CharField(max_length=50)
    car_name = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.car_name}"
    
class MyElectric(models.Model):
    car_image = models.ImageField(null=True, blank=True)
    hire_amount = models.FloatField(default=0)
    location = models.CharField(max_length=50)
    car_name = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.car_name}"
    
