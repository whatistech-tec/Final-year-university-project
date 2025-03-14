from django.contrib import admin

from djangoql.admin import DjangoQLSearchMixin

from .models import VehicleDetail,RentedVehicle,Stories



admin.site.register(VehicleDetail)

class VehicleDetailAdmin(DjangoQLSearchMixin,admin.ModelAdmin):
    list_display = ['plate_number','vehicle_name','vehicle_color','vehicle_category','milage','speed','settings','seats','location','hire_amount','in_stock']

admin.site.register(RentedVehicle)
admin.site.register(Stories)
# admin.site.register(UsersInfo)
