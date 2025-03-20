
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm,CreateRecordForm,UpdateRecordForm,CreateStoryForm,UpdateStoryForm,CreateRentalForm,UpdateRentalForm,PaymentForm
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# to activate the user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from datetime import datetime

#getting token from utils.py
from .utils import TokenGenerator,generate_token
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

#email import
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

#threading
import threading
import requests, base64, json, re, os

from .models import VehicleDetail,RentedVehicle,Stories,UsersInfo,Transaction
from .admin import VehicleDetailAdmin

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
CALLBACK_URL = os.getenv("CALLBACK_URL")
MPESA_BASE_URL = os.getenv("MPESA_BASE_URL")

def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        national_id = request.POST.get('national_id')
        total_quantity = request.POST.get('total_quantity')
        total_price = request.POST.get('total_price')

        # Save to the RentedVehicle model
        rental = RentedVehicle.objects.create(
            first_name=full_name,
            phone=phone,
            address=address,
            company_branch=city,
            transaction_id=national_id,
            total_quantity=total_quantity,
            hire_amount=total_price
        )
        rental.save()

        return redirect('all_rentals')  # Redirect to the rentals page after submission

    return render(request, 'mainapp/checkout.html')
 
 
def all_rentals(request):
    my_rentals = RentedVehicle.objects.all()
    return render(request, 'mainapp/all_rentals.html', {'my_rentals': my_rentals})       

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract details
            full_name = data.get('name')
            phone = data.get('phone')
            address = data.get('address')
            city = data.get('city')
            national_id = data.get('national_id')
            total_quantity = data.get('total_quantity')
            price_per_car = data.get('price_per_car')
            grand_total = data.get('grand_total')
            plate_number = data.get('plate_number')
            vehicle_model = data.get('vehicle_model')
            vehicle_color = data.get('vehicle_color')
            mpesa_code = data.get('mpesa_code')

            # Save to the database
            RentedVehicle.objects.create(
                first_name=full_name,
                phone=phone,
                address=address,
                company_branch=city,
                transaction_id=mpesa_code,
                hire_amount=grand_total,
                car_model=vehicle_model,
                plate_number=plate_number,
                car_color=vehicle_color,
                status="Success"
            )

            return JsonResponse({"status": "success", "message": "Rental data saved successfully!"})

        except Exception as e:
            print(f"Error during checkout: {str(e)}")
            return JsonResponse({"status": "error", "message": f"Failed to save rental data. Error: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


@csrf_exempt
def make_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            amount = data.get('amount')

            # Simulate a successful payment (replace with actual Mpesa logic)
            mpesa_code = "MPESA123456"  # Replace with the actual code from Mpesa response

            return JsonResponse({"status": "success", "mpesa_code": mpesa_code})

        except Exception as e:
            print(f"Error during payment: {str(e)}")
            return JsonResponse({"status": "error", "error_message": f"Payment failed. Error: {str(e)}"})

    return JsonResponse({"status": "error", "error_message": "Invalid request method"})

# Generate M-Pesa access token
def generate_access_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
        }
        response = requests.get(
            f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers,
            timeout=10  # Add a timeout to avoid hanging
        )

        response_data = response.json()
        print("Access Token Response:", response_data)

        if "access_token" in response_data:
            return response_data["access_token"]
        else:
            raise Exception(f"Access token error: {response_data}")

    except requests.RequestException as e:
        print(f"Failed to connect to M-Pesa: {str(e)}")
        return None

# Initiate STK Push and handle response
def initiate_stk_push(phone, amount):
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "Rental Payment",
            "TransactionDesc": "Car Rental Payment",
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=request_body,
            headers=headers,
        ).json()

        print("STK Push Response:", response)  # Debugging line
        return response

    except Exception as e:
        print(f"Failed to initiate STK Push: {str(e)}")
        return {"error": str(e)}

# Phone number formatting and validation
def format_phone_number(phone):
    phone = phone.replace("+", "")
    if re.match(r"^254\d{9}$", phone):
        return phone
    elif phone.startswith("0") and len(phone) == 10:
        return "254" + phone[1:]
    else:
        raise ValueError("Invalid phone number format")


from django.http import JsonResponse

def payment_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = format_phone_number(data.get("phone_number"))
            amount = data.get("amount")
            response = initiate_stk_push(phone, amount)
            print(response)

            if response.get("ResponseCode") == "0":
                checkout_request_id = response["CheckoutRequestID"]
                return JsonResponse({"status": "success", "checkout_request_id": checkout_request_id})
            else:
                error_message = response.get("errorMessage", "Failed to send STK push.")
                return JsonResponse({"status": "failed", "error_message": error_message})

        except ValueError as e:
            return JsonResponse({"status": "failed", "error_message": str(e)})
        except Exception as e:
            return JsonResponse({"status": "failed", "error_message": f"Unexpected error: {str(e)}"})

    return JsonResponse({"status": "failed", "error_message": "Invalid request method"})


@csrf_exempt  # To allow POST requests from external sources like M-Pesa
def payment_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed")

    try:
        callback_data = json.loads(request.body)  # Parse the request body
        result_code = callback_data["Body"]["stkCallback"]["ResultCode"]

        if result_code == 0:
            # Successful transaction
            checkout_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
            metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

            amount = next(item["Value"] for item in metadata if item["Name"] == "Amount")
            mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
            phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

            # Save transaction to the database
            Transaction.objects.create(
                amount=amount, 
                checkout_id=checkout_id, 
                mpesa_code=mpesa_code, 
                phone_number=phone, 
                status="Success"
            )
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment successful"})

        # Payment failed
        return JsonResponse({"ResultCode": result_code, "ResultDesc": "Payment failed"})

    except (json.JSONDecodeError, KeyError) as e:
        return HttpResponseBadRequest(f"Invalid request data: {str(e)}")


# Query STK Push status
def query_stk_push(checkout_request_id):
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
            json=request_body,
            headers=headers,
        )
        print(response.json())
        return response.json()

    except requests.RequestException as e:
        print(f"Error querying STK status: {str(e)}")
        return {"error": str(e)}


# View to query the STK status and return it to the frontend
def stk_status_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            checkout_request_id = data.get('checkout_request_id')
            print("CheckoutRequestID:", checkout_request_id)

            # Query the STK push status using your backend function
            status = query_stk_push(checkout_request_id)

            # Return the status as a JSON response
            return JsonResponse({"status": status})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



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
    context={}
    return render(request, 'mainapp/dash_board.html', context=context)

def maps(request):
    
    return render(request, 'mainapp/maps.html')

def sona_invoice(request):
    
    return render(request, 'mainapp/sona_invoice.html')

def search_form(request):
    
    return render(request, 'mainapp/search_form.html')

def checkout(request):

    return render(request, 'mainapp/checkout.html')

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
def rental_list(request):
    my_rentals = RentedVehicle.objects.all().order_by('-creation_date')
    return render(request, 'mainapp/all_rentals.html', {'my_rentals': my_rentals})

@login_required(login_url='admin_login')
def all_stories(request):
    
    my_stories = Stories.objects.all()

    context = {'my_stories':my_stories}

    return render(request, 'mainapp/all_stories.html', context=context)
def get_users(request):
    
    my_users = UsersInfo.objects.all()

    context = {'my_users':my_users}

    return render(request, 'mainapp/get_users.html', context=context)
   
def pending(request):
    
    return render(request, 'mainapp/pending.html')
   

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
@csrf_exempt
@login_required(login_url='admin_login')
def delete_detail(request, pk):
    
    detail = VehicleDetail.objects.get(id=pk)

    detail.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("all_vehicles")

@csrf_exempt
@login_required(login_url='admin_login')
def delete_story(request, pk):
    
    my_stories = Stories.objects.get(id=pk)

    my_stories.delete()

    messages.success(request, "Your story was deleted!")


    return redirect("all_stories")

@csrf_exempt
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

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')

def admin_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/admin_login')



    