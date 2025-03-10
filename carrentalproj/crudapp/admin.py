from django.contrib import admin
from mainapp.models import MyCars,MyVans,MySuvs,MyElectric
from . models import Record, AllVehicles

admin.site.register(Record)
admin.site.register(AllVehicles)
