from django.db import models

from mainapp.models import MyCars, MyVans, MySuvs, MyElectric

# Create your models here.
class Record(models.Model):
    
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
    
class AllVehicles(models.Model):
    
    company_branch = models.CharField(max_length=255, default='')

    car_model = models.CharField(max_length=200, default='')

    plate_number = models.CharField(max_length=200, default='')

    car_color = models.CharField(max_length=200, default='')
    
    images = models.ImageField(upload_to='media/',default="")
    
    available = models.BooleanField(default=True)
    
    hire_amount = models.FloatField(default=0)

   
    def __str__(self):

        return self.car_model + "   " + self.car_color