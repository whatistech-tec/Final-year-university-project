from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm, UploadVehicle

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import Record,AllVehicles,MyCars,MyVans,MySuvs,MyElectric

def home(request):
   
    return render(request, 'index.html')


#Register

def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successifully!")

            return redirect("my-login")

    context = {'form': form}  

    return render(request, 'register.html', context=context)       

#login

def my_login(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                messages.success(request, "You have logged in successifully!")

                return redirect("all")

    context = {'form':form}
    return render(request, 'my-login.html', context=context)


#Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'dashboard.html', context=context)

@login_required(login_url='my-login')
def search_venue(request):

    if request.method == "POST":
        searched = request.POST['searched']
        records = Record.objects.filter(plate_number__contains=searched)

        return render(request, 'search_venue.html', {'searched':searched},{'records':records})

    else:
        return render(request, 'search_venue.html', context=context)
#logout

def cars(request):
    cars_category = MyCars.objects.all()
    return render(request, "my-cars.html", {'cars_category':cars_category})

def vans(request):
    vans_category = MyVans.objects.all()
    return render(request, "my-vans.html", {'vans_category':vans_category})

def electric(request):
    electric_category = MyElectric.objects.all()
    return render(request, "my-electrics.html", {'electric_category':electric_category})
def suvs(request):
    suvs_category = MySuvs.objects.all()
    return render(request, "my-suvs.html", {'suvs_category':suvs_category})


def all(request):
    all_vehicles = AllVehicles.objects.all()
    return render(request, "all.html", {'all_vehicles':all_vehicles})

@login_required(login_url='my-login')
def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")

#create a record

@login_required(login_url='my-login')
def upload_vehicle(request): 

    form = UploadVehicle()

    if request.method == "POST":

        form = UploadVehicle(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")


            return redirect("dashboard")
                
    context = {"form":form}

    return render(request, 'upload-new-vehicle.html', context=context)

@login_required(login_url='my-login')
def create_record(request): 

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")


            return redirect("dashboard")
                
    context = {"form":form}

    return render(request, 'create-record.html', context=context)

#update a record

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method =='POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard")

    context = {'form':form}

    return render(request, 'update-record.html', context=context)


#view a single record

@login_required(login_url='my-login')
def single_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'view-record.html', context=context)

#delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")


    return redirect("dashboard")