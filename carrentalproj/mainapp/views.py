
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm,CreateRecordForm,UpdateRecordForm,CreateStoryForm,UpdateStoryForm,CreateRentalForm,UpdateRentalForm
from .cart import Cart
from django.http import JsonResponse


# to activate the user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError

#getting token from utils.py
from .utils import TokenGenerator,generate_token

#email import
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

#threading
import threading


from .models import VehicleDetail,RentedVehicle,Stories
from .filters import VehicleDetailFilter, RentedVehicleFilter, StoriesFilter
from .admin import VehicleDetailAdmin


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()   

def auth(request):
    if request.method=="POST":
        # username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.error(request,"Password is Not Matching")
            return render(request,'mainapp/auth.html')                   
        try:
            if User.objects.get(username=email):
                messages.error(request,"Email Already Taken!")
                return render(request,'mainapp/auth.html')
              
        except Exception as identifier:
             pass

        user = User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subject="Activate Your Account"
        message=render_to_string('mainapp/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.success(request,"Activate account by clicking link on your email ")
        return redirect('/login')
    
    context={}
    return render(request, "mainapp/auth.html", context)

class ActivateAccountView(View):
    def get(self, request, uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.sucess(request, "Account activated successifully!")
            return redirect('/login')
        return render(request,'activatefail.html')


def handlelogin(request):
    if request.method=="POST":
        
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request, myuser)
            messages.success(request,"Login Success")
            return render(request, 'mainapp/home.html')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    context={}
    return render(request, "mainapp/login.html", context)


#login

def admin_login(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                messages.success(request, "You have logged in successifully!")

                return redirect("dash_board")

    context = {'form':form}
    return render(request, 'mainapp/admin_login.html', context=context)

@login_required(login_url='admin_login')
def dash_board(request):

    return render(request, 'mainapp/dash_board.html', context=context)

@login_required(login_url='admin_login')
def vehicle_categories(request,foo):
    # foo = foo.replace('-',' ')
    try:
        vehicle_category = Category.objects.get(category_name=foo)
        vehicle_detail = VehicleDetail.objects.filter(vehicle_category=vehicle_category)
        return render(request, 'mainapp/vehicle_categories.html', {'vehicle_detail':vehicle_detail,'vehicle_category':vehicle_category})
    except:
        messages.success(request,("That Category Doesn't Exist!"))
        return redirect('all_vehicles')


@login_required(login_url='admin_login')
def all_vehicles(request):
    
    cars = VehicleDetail.objects.filter(vehicle_category__iexact='car')
    suvs = VehicleDetail.objects.filter(vehicle_category__iexact='suv')
    vans = VehicleDetail.objects.filter(vehicle_category__iexact='van')
    electrics = VehicleDetail.objects.filter(vehicle_category__iexact='electric')

    context = {
        'cars': cars,
        'suvs': suvs,
        'vans': vans,
        'electrics': electrics,
    }
    return render(request, 'mainapp/all_vehicles.html', context=context)

def admin_cars(request):
    cars = VehicleDetail.objects.filter(vehicle_category__iexact='car')
    return render(request, 'mainapp/admin_cars.html', {'vehicles': cars})

def admin_suvs(request):
    suvs = VehicleDetail.objects.filter(vehicle_category__iexact='suv')
    return render(request, 'mainapp/admin_suvs.html', {'vehicles': suvs})

def admin_vans(request):
    vans = VehicleDetail.objects.filter(vehicle_category__iexact='van')
    return render(request, 'mainapp/admin_vans.html', {'vehicles': vans})

def admin_electrics(request):
    electric_cars = VehicleDetail.objects.filter(vehicle_category__iexact='electric')
    return render(request, 'mainapp/admin_electrics.html', {'vehicles': electric_cars})


def cars(request):
    cars = VehicleDetail.objects.filter(vehicle_category__iexact='car')
    return render(request, "mainapp/cars.html", {'vehicles': cars})

def suvs(request):
    suvs = VehicleDetail.objects.filter(vehicle_category__iexact='suv')
    return render(request, "mainapp/vans.html", {'vehicles': suvs})

def vans(request):
    vans = VehicleDetail.objects.filter(vehicle_category__iexact='van')
    return render(request, "mainapp/electric.html", {'vehicles': vans})
def electric(request):
    electric_cars = VehicleDetail.objects.filter(vehicle_category__iexact='electric')
    return render(request, "mainapp/suvs.html", {'vehicles': electric_cars})


@login_required(login_url='admin_login')
def all_rentals(request):
    
    my_rentals = RentedVehicle.objects.all()

    context = {'my_rentals':my_rentals}

    return render(request, 'mainapp/all_rentals.html', context=context)

@login_required(login_url='admin_login')
def all_stories(request):
    
    my_stories = Stories.objects.all()

    context = {'my_stories':my_stories}

    return render(request, 'mainapp/all_stories.html', context=context)
   

@login_required(login_url='admin_login')
def create_record(request): 

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")


            return redirect("all_vehicles")
                
    context = {"form":form}

    return render(request, 'mainapp/create_record.html', context=context)


@login_required(login_url='admin_login')
def create_story(request): 

    form = CreateStoryForm()

    if request.method == "POST":

        form = CreateStoryForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, "Your story was created!")


            return redirect("all_stories")
                
    context = {"form":form}

    return render(request, 'mainapp/create_story.html', context=context)


@login_required(login_url='admin_login')
def create_rental(request): 

    form = CreateRentalForm()

    if request.method == "POST":

        form = CreateRentalForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your your rental went through successifully!")


            return redirect("all_rentals")
                
    context = {"form":form}

    return render(request, 'mainapp/create_rental.html', context=context)

#update a record


@login_required(login_url='admin_login')
def update_record(request, pk):
    
    record = VehicleDetail.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method =='POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("all_vehicles")

    context = {'form':form}

    return render(request, 'mainapp/update_record.html', context=context)


@login_required(login_url='admin_login')
def update_story(request, pk):
    
    my_stories = Stories.objects.get(id=pk)

    form = UpdateStoryForm(instance=my_stories)

    if request.method =='POST':

        form = UpdateStoryForm(request.POST, instance=my_stories)

        if form.is_valid():

            form.save()

            messages.success(request, "Your story was updated!")

            return redirect("all_stories")

    context = {'form':form}

    return render(request, 'mainapp/update_story.html', context=context)


@login_required(login_url='admin_login')
def update_rental(request, pk):

    my_rental = RentedVehicle.objects.get(id=pk)

    form = UpdateRentalForm(instance=my_rental)

    if request.method =='POST':

        form = UpdateRentalForm(request.POST, instance=my_rental)

        if form.is_valid():

            form.save()

            messages.success(request, "Your rental info was updated!")

            return redirect("all_rentals")

    context = {'form':form}

    return render(request, 'mainapp/update_rental.html', context=context)

#view a single record

@login_required(login_url='admin_login')
def single_record(request, pk):
    
    all_records = VehicleDetail.objects.get(id=pk)

    context = {'detail':all_records}

    return render(request, 'mainapp/view_record.html', context=context)


@login_required(login_url='admin_login')
def view_story(request, pk):
    
    my_stories = Stories.objects.get(id=pk)

    context = {'story':my_stories}

    return render(request, 'mainapp/view_story.html', context=context)


@login_required(login_url='admin_login')
def view_rental(request, pk):

    my_rentals = RentedVehicle.objects.get(id=pk)

    context = {'rental':my_rentals}

    return render(request, 'mainapp/view_rental.html', context=context)



#delete a record

@login_required(login_url='admin_login')
def delete_detail(request, pk):
    
    detail = VehicleDetail.objects.get(id=pk)

    detail.delete()

    messages.success(request, "Your record was deleted!")


    return redirect("all_vehicles")


@login_required(login_url='admin_login')
def delete_story(request, pk):
    
    my_stories = Stories.objects.get(id=pk)

    my_stories.delete()

    messages.success(request, "Your story was deleted!")


    return redirect("all_stories")


@login_required(login_url='admin_login')
def delete_rental(request, pk):

    rental = RentedVehicle.objects.get(id=pk)

    rental.delete()

    messages.success(request, "Your rental info was deleted!")


    return redirect("all_rentals")




#filters

@login_required(login_url='admin_login')
def filtered_vehicles(request):
    
    vehicles = VehicleDetail.objects.all()
    
    vehicle_filter = VehicleDetailFilter(request.GET, queryset=vehicles)

    return render(request, "mainapp/filtered_vehicles.html", {'vehicle_filter':vehicle_filter})


@login_required(login_url='admin_login')
def search_vehicles(request):
    
    vehicles = VehicleDetail.objects.all()
    
    vehicle_filter = VehicleDetailAdmin(request.GET, queryset=vehicles)

    return render(request, "mainapp/filtered_vehicles.html", {'vehicle_filter':vehicle_filter})


def home(request):
    context={}
    return render(request, "mainapp/home.html", context)

def dash_board(request):
    return render(request, 'mainapp/dash_board.html')

def rent_now(request):
    return render(request, 'mainapp/rent_now.html')

def search(request):
    context={}
    return render(request, "mainapp/search.html", context)

def rent(request):
    renting_cars = VehicleDetail.objects.all()
    return render(request, "mainapp/rent.html", {'renting_cars':renting_cars})

def ride(request):
    context={}
    return render(request, "mainapp/ride.html", context)

def stories(request):
    my_stories = Stories.objects.all()
    context = {'my_stories':my_stories}
    return render(request, 'mainapp/stories.html', context=context)


def contact(request):
    context={}
    return render(request, "mainapp/contact.html", context)


# def get_users(request):
    
#     user_details = UsersInfo.objects.all()

#     context = {'user_details':user_details}

#     return render(request, 'mainapp/get_users.html', context=context)

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')

def admin_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/admin_login')


#cart
def cart_summary(request):
    
    return render(request, "mainapp/cart_summary.html")

def add_to_cart(request):
    cart = Cart(request)
    if request.POST.get(action) == 'post':
        detail_id = int(request.POST.get('detail_id'))
        detail = get_object_or_404(VehicleDetail,id=detail_id)
        cart.add(detail=detail)
        
        response = JsonResponse({'Car Name':detail.vehicle_name})
        return response

def delete_from_cart(request):
    pass

def update_cart(request):
    pass