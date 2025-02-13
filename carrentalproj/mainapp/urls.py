from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name="home"),
    path('auth', views.auth, name="auth"),
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
