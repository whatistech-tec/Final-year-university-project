from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from .models import VehicleDetail,RentedVehicle, Stories

from django.forms.widgets import PasswordInput, TextInput


#Login user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#create a record
class CreateRecordForm(forms.ModelForm):

    class Meta:

        model = VehicleDetail
        fields = [ 'vehicle_image', 'plate_number', 'vehicle_name', 'vehicle_color', 'vehicle_category', 'milage','speed','settings','seats','location','hire_amount']
        
#update a record
class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = VehicleDetail
        fields = [ 'vehicle_image', 'plate_number', 'vehicle_name', 'vehicle_color', 'vehicle_category', 'milage','speed','settings','seats','location','hire_amount']
        
#stories
class CreateStoryForm(forms.ModelForm):
    
    class Meta:

        model = Stories
        fields = [ 'story_image', 'date', 'month', 'year', 'header', 'story']
        
class UpdateStoryForm(forms.ModelForm):

    class Meta:

        model = Stories
        fields = [ 'story_image', 'date', 'month', 'year', 'header', 'story']
        
class CreateRentalForm(forms.ModelForm):
    
    class Meta:
    
        model = RentedVehicle
        fields = [ 'first_name', 'last_name', 'email', 'phone', 'address', 'company_branch','car_model','plate_number','car_color','agent_name','agent_number']
        
class UpdateRentalForm(forms.ModelForm):
    
    class Meta:
    
        model = RentedVehicle
        fields = [ 'first_name', 'last_name', 'email', 'phone', 'address', 'company_branch','car_model','plate_number','car_color','agent_name','agent_number']
        
