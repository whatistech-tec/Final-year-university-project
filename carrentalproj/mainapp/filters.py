import django_filters

from .models import VehicleDetail, RentedVehicle,Stories

class VehicleDetailFilter(django_filters.FilterSet):
    
    class Meta:
        model = VehicleDetail
        fields = {
            
            'plate_number': ['exact'],
            'vehicle_name': ['exact'],
            'vehicle_color': ['exact'],
            'vehicle_category': ['exact'],
            'milage': ['lt','gt'],
            # 'speed': ['lt','gt'],
            # 'settings': ['lt','gt'],
            'seats': ['exact'],
            'location': ['exact'],
            'hire_amount': ['lt','gt'],
        }
class RentedVehicleFilter(django_filters.FilterSet):
    
    class Meta:
        model = RentedVehicle
        fields = {
            
            'first_name': ['exact'],
            'last_name': ['exact'],
            'email': ['exact'],
            'phone': ['exact'],
            'address': ['exact'],
            'company_branch': ['exact'],
            'car_model': ['exact'],
            'plate_number': ['exact'],
            'car_color': ['exact'],
            'agent_name': ['exact'],
            'agent_number': ['lt','gt'],
           
        }
class StoriesFilter(django_filters.FilterSet):
    
    class Meta:
        model = Stories
        fields = {
            
            'header': ['exact'],
            'month': ['lt','gt'],
            'year': ['lt','gt'],
            
        }