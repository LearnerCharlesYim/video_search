from django.urls import path
from . import views

urlpatterns = [
    path(r'login/$', views.login, name='login'),
    path(r'register/$', views.register, name='register'),
    path(r'logout/$', views.logout, name='logout'),
    path(r'^serch/$', views.serch, name='serch'),
    path(r'', views.index, name="index"),
    path('detail/<video_id>/', views.video_detail, name="video_detail"),

]
