
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm,CreateRecordForm,UpdateRecordForm,CreateStoryForm,UpdateStoryForm,CreateRentalForm,UpdateRentalForm,PaymentForm
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
from decimal import Decimal
#threading
import threading
import requests, base64, json, re, os

from .models import VehicleDetail,RentedVehicle,Stories,UsersInfo,Transaction
from .admin import VehicleDetailAdmin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
CALLBACK_URL = os.getenv("CALLBACK_URL")
MPESA_BASE_URL = os.getenv("MPESA_BASE_URL")




from django.db.models import Q

def vehicle_search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    vehicles = VehicleDetail.objects.filter(
        Q(vehicle_name__icontains=query) |
        Q(plate_number__icontains=query) |
        Q(vehicle_color__icontains=query) |
        Q(vehicle_category__icontains=query) |
        Q(location__icontains=query)
    ).order_by('-creation_date')

    return render(request, 'mainapp/vehicle_search.html', {'vehicles': vehicles, 'query': query})

def frontend_vehicle_search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    vehicles = VehicleDetail.objects.filter(
        Q(vehicle_name__icontains=query) |
        Q(vehicle_color__icontains=query) |
        Q(vehicle_category__icontains=query) |
        Q(location__icontains=query)
    ).order_by('-creation_date')

    return render(request, 'mainapp/frontend_vehicle_search.html', {'vehicles': vehicles, 'query': query})

@csrf_exempt
def toggle_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plate_number = data.get('plate_number')

            # Fetch the vehicle by plate number
            vehicle = VehicleDetail.objects.get(plate_number=plate_number)

            # Toggle the availability status
            vehicle.in_stock = not vehicle.in_stock
            vehicle.save()

            return JsonResponse({'status': 'success', 'in_stock': vehicle.in_stock})
        
        except VehicleDetail.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Vehicle not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def payment_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Extract customer details
            name = data.get('name', '')
            phone_number = format_phone_number(data.get("phone"))
            address = data.get('address', '')
            city = data.get('city', '')
            national_id = data.get('nationalId', '')

            # Extract vehicle details
            cart_items = data.get('cart', {})
            first_vehicle = list(cart_items.values())[0] if cart_items else {}
            vehicle_name = first_vehicle.get('name', '')
            vehicle_color = first_vehicle.get('color', '')
            plate_number = first_vehicle.get('plateNumber', '')

            # Rental details
            pickup_date = data.get('pickupDate', None)
            return_date = data.get('returnDate', None)
            rental_days = int(data.get('rentalDays', 1))

            # Financial details
            subtotal = Decimal(str(data.get('subtotal', 0)))
            vat = Decimal(str(data.get('vat', 0)))
            discount = Decimal(str(data.get('discount', 0)))
            final_total = Decimal(str(data.get('total', 0)))
            hire_amount = subtotal  # Assuming this is the base rental cost
            amount = final_total  # Total after VAT & discount

            response = initiate_stk_push(phone_number, float(amount))


            # Save transaction
            transaction = Transaction.objects.create(
                name=name,
                phone_number=phone_number,
                address=address,
                city=city,
                national_id=national_id,
                amount=amount,
                hire_amount=hire_amount,
                vehicle_name=vehicle_name,
                vehicle_color=vehicle_color,
                plate_number=plate_number,
                rental_days=rental_days,
                pickup_date=pickup_date,
                return_date=return_date,
                subtotal=subtotal,
                vat=vat,
                discount=discount,
                final_total=final_total
            )

            # Mark vehicle as unavailable
            VehicleDetail.objects.filter(plate_number=plate_number).update(in_stock=False)

            return JsonResponse({"success": True, "transaction_id": transaction.id, "message": "Payment saved successfully!"})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

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
def initiate_stk_push(phone_number, amount):
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
            "PartyA": phone_number,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "SONA PREMIUM",
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
    try:
        phone = phone.replace("+", "")
        if re.match(r"^254\d{9}$", phone):
            return phone
        elif phone.startswith("0") and len(phone) == 10:
            return "254" + phone[1:]
        else:
            raise ValueError("Invalid phone number format")
    except Exception as e:
        raise ValueError(f"Error formatting phone number: {str(e)}")



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
            transactionCode = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
            phone_number = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

            # Save transaction to the database
            Transaction.objects.create(
                amount=amount, 
                checkout_id=checkout_id, 
                transactionCode=transactionCode, 
                phone_number=phone_number, 
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

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

generate_token = TokenGenerator()

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
            messages.success(request, "Account activated successifully!")
            return redirect('/login')
        return render(request,'mainapp/activatefail.html')


class ReqiuestResetEmailView(View):
    def get(self,request):
        return render(request, 'mainapp/request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)
        
        if user.exists():
            current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message = render_to_string('mainapp/reset-user-password.html',
            {
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])

            })
            
            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            EmailThread(email_message).start()
            
            messages.info(request,"WE SENT YOU AN EMAIL WITH INSTRUCTIONS TO RESET YOUR PASSWORD")
            return render(request,'mainapp/request-reset-email.html')
        
        
class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid!")
                return render(request,'mainapp/request-reset-email.html')
            
        except DjangoUnicodeDecodeError as identifier:
            pass
        
        return render(request,'mainapp/set-new-password.html',context)
    
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'mainapp/set-new-password.html',context)
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success! Please login with the new password")  
            return redirect('/login/')
        
        except DjangoUnicodeDecodeError as identifier:
            messges.error(request,"Something Went Wrong!")
            return render(request,'mainapp/set-new-password.html',context)


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



def sona_invoice(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    # transaction.cart = json.loads(transaction.cart)
    return render(request, "mainapp/sona_invoice.html", {"transaction": transaction})


def incoming_client(request):
    my_clients = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'mainapp/incoming_client.html',{'my_clients':my_clients})

def search_form(request):
    
    return render(request, 'mainapp/search_form.html')

def checkout(request):

    return render(request, 'mainapp/checkout.html')

@login_required(login_url='admin_login')

def all_vehicles(request):
    vehicles = VehicleDetail.objects.all().order_by('-creation_date')
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'mainapp/all_vehicles.html', context=context)

def admin_cars(request):
    cars = VehicleDetail.objects.filter(vehicle_category__iexact='car').order_by('-creation_date')
    return render(request, 'mainapp/admin_cars.html', {'vehicles': cars})

def admin_suvs(request):
    suvs = VehicleDetail.objects.filter(vehicle_category__iexact='suv').order_by('-creation_date')
    return render(request, 'mainapp/admin_suvs.html', {'vehicles': suvs})

def admin_vans(request):
    vans = VehicleDetail.objects.filter(vehicle_category__iexact='van').order_by('-creation_date')
    return render(request, 'mainapp/admin_vans.html', {'vehicles': vans})


def admin_electrics(request):
    electric_cars = VehicleDetail.objects.filter(vehicle_category__iexact='electric').order_by('-creation_date')
    return render(request, 'mainapp/admin_electrics.html', {'vehicles': electric_cars})

def admin_electrics(request):
    electric_cars = VehicleDetail.objects.filter(vehicle_category__iexact='electric').order_by('-creation_date')
    return render(request, 'mainapp/admin_electrics.html', {'vehicles': electric_cars})


def cars(request):
    cars = VehicleDetail.objects.filter(vehicle_category__iexact='car').order_by('-creation_date')
    return render(request, "mainapp/cars.html", {'vehicles': cars})

def suvs(request):
    suvs = VehicleDetail.objects.filter(vehicle_category__iexact='suv').order_by('-creation_date')
    return render(request, "mainapp/vans.html", {'vehicles': suvs})

def vans(request):
    vans = VehicleDetail.objects.filter(vehicle_category__iexact='van').order_by('-creation_date')
    return render(request, "mainapp/electric.html", {'vehicles': vans})
def electric(request):
    electric_cars = VehicleDetail.objects.filter(vehicle_category__iexact='electric').order_by('-creation_date')
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


def home(request):
    context={}
    return render(request, "mainapp/home.html", context)

def dash_board(request):
    return render(request, 'mainapp/dash_board.html')

def rent_now(request):
    return render(request, 'mainapp/rent_now.html')


def rent(request):
    renting_cars = VehicleDetail.objects.all()
    prices = list(renting_cars.values_list('hire_amount', flat=True))  # Get the list of prices
    return render(request, 'mainapp/rent.html', {'renting_cars': renting_cars, 'hire_amount': prices})


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



    