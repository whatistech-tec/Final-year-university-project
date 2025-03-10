from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from .models import VehicleDetail

from django.forms.widgets import PasswordInput, TextInput


#Login user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#create a record
class CreateRecordForm(forms.ModelForm):

    class Meta:

        model = VehicleDetail
        fields = [ 'vehicle_image', 'plate_number', 'vehicle_name', 'vehicle_color', 'vehicle_category', 'location','hire_amount']
        
#update a record
class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = VehicleDetail
        fields = [ 'vehicle_image', 'plate_number', 'vehicle_name', 'vehicle_color', 'vehicle_category', 'location','hire_amount']
