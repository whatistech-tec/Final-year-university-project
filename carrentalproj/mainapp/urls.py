from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name="home"),
    path('dash_board', views.dash_board, name="dash_board"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('all_vehicles', views.all_vehicles, name="all_vehicles"),
    path('rent_now', views.rent_now, name="rent_now"),
    # path('get_users', views.get_users, name="get_users"),
    path('filtered_vehicles', views.filtered_vehicles, name="filtered_vehicles"),
    path('filtered_vehicles', views.search_vehicles, name="filtered_vehicles"),
    path('all_rentals', views.all_rentals, name="all_rentals"),
    path('all_stories', views.all_stories, name="all_stories"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('create_record', views.create_record, name="create_record"),
    path('create_story', views.create_story, name="create_story"),
    path('create_rental', views.create_rental, name="create_rental"),
    path('update_record/<int:pk>', views.update_record, name="update_record"),
    path('update_story/<int:pk>', views.update_story, name="update_story"),
    path('update_rental/<int:pk>', views.update_rental, name="update_rental"),
    path('view_record/<int:pk>', views.single_record, name="view_record"),
    path('vehicle_categories/<str:foo>', views.vehicle_categories, name="vehicle_categories"),

    path('view_story/<int:pk>', views.view_story, name="view_story"),
    path('view_rental/<int:pk>', views.view_rental, name="view_rental"),
    path('delete_detail/<int:pk>', views.delete_detail, name="delete_detail"),
    path('delete-story/<int:pk>', views.delete_story, name="delete-story"),
    path('delete-rental/<int:pk>', views.delete_rental, name="delete_rental"),

    path('auth', views.auth, name="auth"),
    path('login', views.handlelogin, name="login"),
    path('logout', views.handlelogout, name="handlelogout"),
    
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate'),
    # path('request-reset-email/',views.ReqiuestResetEmailView.as_view(), name='request-reset-email'),
    # path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(), name='set-new-password'),
    
    path('search', views.search, name="search"),
    path('rent', views.rent, name="rent"),
    path('ride', views.ride, name="ride"),
    path('stories', views.stories, name="stories"),
    path('cars', views.cars, name="cars"),
    path('suvs', views.suvs, name="suvs"),
    path('vans', views.vans, name="vans"),
    path('electric', views.electric, name="electric"),
    path('contact', views.contact, name="contact"),
    
    path('admin_cars/', views.admin_cars, name='admin_cars'),
    path('admin_suvs/', views.admin_suvs, name='admin_suvs'),
    path('admin_vans/', views.admin_vans, name='admin_vans'),
    path('admin_electrics/', views.admin_electrics, name='admin_electrics'),
    
    
    #cart
    path('cart_summary', views.cart_summary, name="cart_summary"),
    # path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('delete_from_cart', views.delete_from_cart, name="delete_from_cart"),
    path('update_cart', views.update_cart, name="update_cart"),
    
 
 
]
