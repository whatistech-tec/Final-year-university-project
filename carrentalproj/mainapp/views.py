from django.shortcuts import render
from .models import MyCars,MyVans,MySuvs,MyElectric,ForRent,Stories


def home(request):
    context={}
    return render(request, "mainapp/home.html", context)

def auth(request):
    context={}
    return render(request, "mainapp/auth.html", context)

def search(request):
    context={}
    return render(request, "mainapp/search.html", context)

def rent(request):
    renting_cars = ForRent.objects.all()
    return render(request, "mainapp/rent.html", {'renting_cars':renting_cars})

def ride(request):
    context={}
    return render(request, "mainapp/ride.html", context)

def stories(request):
    item_card = Stories.objects.all()
    context={}
    return render(request, "mainapp/stories.html", {'item_card':item_card})

def cars(request):
    cars_category = MyCars.objects.all()
    return render(request, "mainapp/cars.html", {'cars_category':cars_category})

def vans(request):
    vans_category = MyVans.objects.all()
    return render(request, "mainapp/vans.html", {'vans_category':vans_category})

def electric(request):
    electric_category = MyElectric.objects.all()
    return render(request, "mainapp/electric.html", {'electric_category':electric_category})
def suvs(request):
    suvs_category = MySuvs.objects.all()
    return render(request, "mainapp/suvs.html", {'suvs_category':suvs_category})

def contact(request):
    context={}
    return render(request, "mainapp/contact.html", context)