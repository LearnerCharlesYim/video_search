from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('', views.index, name="index"),
    path('detail/<video_id>/', views.video_detail, name="video_detail"),

]
