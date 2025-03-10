from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name="home"),
    path('dash_board', views.dash_board, name="dash_board"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('all_vehicles', views.all_vehicles, name="all_vehicles"),
    path('all_stories', views.all_stories, name="all_stories"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('create_record', views.create_record, name="create_record"),
    path('create_story', views.create_story, name="create_story"),
    path('update_record/<int:pk>', views.update_record, name="update_record"),
    path('update_story/<int:pk>', views.update_story, name="update_story"),
    path('view_record/<int:pk>', views.single_record, name="view_record"),
    path('view_story/<int:pk>', views.view_story, name="view_story"),
    path('delete-detail/<int:pk>', views.delete_detail, name="delete-detail"),
    path('delete-story/<int:pk>', views.delete_story, name="delete-story"),

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
 
]
