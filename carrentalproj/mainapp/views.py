
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm,CreateRecordForm,UpdateRecordForm,CreateStoryForm,UpdateStoryForm


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


from .models import VehicleDetail, MyCars,MyVans,MySuvs,MyElectric,ForRent,Stories


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
                auth.login(request, user)

                messages.success(request, "You have logged in successifully!")

                return redirect("dash_board")

    context = {'form':form}
    return render(request, 'mainapp/admin_login.html', context=context)


def dash_board(request):

    return render(request, 'mainapp/dash_board.html', context=context)


def all_vehicles(request):
    
    vehicle_details = VehicleDetail.objects.all()

    context = {'vehicle_details':vehicle_details}

    return render(request, 'mainapp/all_vehicles.html', context=context)

def all_stories(request):
    
    my_stories = Stories.objects.all()

    context = {'my_stories':my_stories}

    return render(request, 'mainapp/all_stories.html', context=context)
   

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

#update a record

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

def update_story(request, pk):

    my_stories = Stories.objects.get(id=pk)

    form = UpdateStoryForm(instance=record)

    if request.method =='POST':

        form = UpdateStoryForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your story was updated!")

            return redirect("all_stories")

    context = {'form':form}

    return render(request, 'mainapp/update_story.html', context=context)

#view a single record

def single_record(request, pk):
    
    all_records = VehicleDetail.objects.get(id=pk)

    context = {'detail':all_records}

    return render(request, 'mainapp/view_record.html', context=context)

def view_story(request, pk):

    my_stories = Stories.objects.get(id=pk)

    context = {'my_stories':my_stories}

    return render(request, 'mainapp/view_story.html', context=context)



#delete a record


def delete_detail(request, pk):
    
    detail = VehicleDetail.objects.get(id=pk)

    detail.delete()

    messages.success(request, "Your record was deleted!")


    return redirect("all_vehicles")

def delete_story(request, pk):

    my_stories = Stories.objects.get(id=pk)

    story.delete()

    messages.success(request, "Your story was deleted!")


    return redirect("all_stories")


def home(request):
    context={}
    return render(request, "mainapp/home.html", context)

def dash_board(request):
    return render(request, 'mainapp/dash_board.html')

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
    my_stories = Stories.objects.all()
    context = {'my_stories':my_stories}
    return render(request, 'mainapp/stories.html', context=context)

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

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')

def admin_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/admin_login')
