from . import views
from django.urls import path, include

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name="home"),
    path('dash_board/', views.dash_board, name="dash_board"),
    #  path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin Authentication
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),
    
    # User Authentication
    path('auth/', views.auth, name="auth"),
    path('login/', views.handlelogin, name="login"),
    path('logout/', views.handlelogout, name="handlelogout"),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),

    # Vehicle Management
    path('all_vehicles/', views.all_vehicles, name="all_vehicles"),
    path('rent_now/', views.rent_now, name="rent_now"),
    path('rent/', views.rent, name="rent"),
    path('ride/', views.ride, name="ride"),
    path('filtered_vehicles/', views.filtered_vehicles, name="filtered_vehicles"),
    path('search_vehicles/', views.search_vehicles, name="search_vehicles"),
    path('search_form/', views.search_form, name="search_form"),
    path('vehicle_categories/<str:foo>/', views.vehicle_categories, name="vehicle_categories"),
    path('search/', views.search, name="search"),
    path('sona_invoice/', views.sona_invoice, name="sona_invoice"),
    # path('submit_rental/', views.submit_rental, name='submit_rental'),

    # Vehicle Categories
    path('cars/', views.cars, name="cars"),
    path('suvs/', views.suvs, name="suvs"),
    path('vans/', views.vans, name="vans"),
    path('electric/', views.electric, name="electric"),
    path('maps/', views.maps, name="maps"),

    # Admin Vehicle Categories
    path('admin_cars/', views.admin_cars, name='admin_cars'),
    path('admin_suvs/', views.admin_suvs, name='admin_suvs'),
    path('admin_vans/', views.admin_vans, name='admin_vans'),
    path('admin_electrics/', views.admin_electrics, name='admin_electrics'),

    # Rentals and Transactions
    path('checkout/', views.checkout, name='checkout'),
    path('all_rentals/', views.rental_list, name="all_rentals"),
    path('create_rental/', views.create_rental, name="create_rental"),
    path('update_rental/<int:pk>/', views.update_rental, name="update_rental"),
    path('view_rental/<int:pk>/', views.view_rental, name="view_rental"),
    path('delete_rental/<int:pk>/', views.delete_rental, name="delete_rental"),
    path('pending/', views.pending, name="pending"),

    # Payment Processing
    path('make_payment/', views.payment_view, name="make_payment"),
    path('callback/', views.payment_callback, name='payment_callback'),

    # Story Management
    path('stories/', views.stories, name="stories"),
    path('all_stories/', views.all_stories, name="all_stories"),
    path('create_story/', views.create_story, name="create_story"),
    path('update_story/<int:pk>/', views.update_story, name="update_story"),
    path('view_story/<int:pk>/', views.view_story, name="view_story"),
    path('delete_story/<int:pk>/', views.delete_story, name="delete_story"),

    # Records Management
    path('create_record/', views.create_record, name="create_record"),
    path('update_record/<int:pk>/', views.update_record, name="update_record"),
    path('view_record/<int:pk>/', views.single_record, name="view_record"),
    path('delete_detail/<int:pk>/delete/', views.delete_detail, name="delete_detail"),

    # User Management
    path('get_users/', views.get_users, name="get_users"),

    # Contact and Support
    path('contact/', views.contact, name="contact"),
]
