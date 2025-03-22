from django.contrib import admin

from djangoql.admin import DjangoQLSearchMixin

from .models import VehicleDetail,RentedVehicle,Stories,Transaction




@admin.register(RentedVehicle)
class RentedVehicleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'phone', 
        'address', 'company_branch', 'car_model', 'plate_number', 
        'car_color', 'hire_amount', 
        'transaction_id', 'status', 'creation_date'
    ]

    list_filter = [
        'status', 'hire_amount', 'creation_date'
    ]
@admin.register(VehicleDetail)
class VehicleDetailAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_name', 'plate_number', 'vehicle_color', 
        'hire_amount', 'in_stock', 'location'
    )
    search_fields = ('vehicle_name', 'plate_number')
    list_filter = ('in_stock', 'location', 'vehicle_category')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number','address', 'city','amount','national_id','vehicle_name','vehicle_color','plate_number' ,'transactionCode','timestamp')
    
admin.site.register(Stories)
