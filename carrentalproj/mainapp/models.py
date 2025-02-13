from django.db import models

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
    
class ForRent(models.Model):
    car_image = models.ImageField(null=True, blank=True, upload_to='rent/')
    milage = models.FloatField(default=0)
    # hire_amount = models.FloatField(default=0)
    speed = models.IntegerField(default=0)
    settings = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    
    car_name = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.car_name}"
    
class Stories(models.Model):
    story_image = models.ImageField(null=True, blank=True, upload_to='stories/')
    date = models.IntegerField(default=0)
    month = models.CharField(max_length=50)
    year = models.IntegerField(default=0)
    header = models.CharField(max_length=50)
    story = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.header}"
