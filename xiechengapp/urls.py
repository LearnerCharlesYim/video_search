from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('', views.index, name="index"),
    path('detail/<video_id>/', views.video_detail, name="video_detail"),
    path(r'pie/', views.ChartView.as_view(), name='pie'),
    path(r'bar/', views.ChartBarView.as_view(), name='bar'),
    path(r'line/', views.ChartLineView.as_view(), name='line'),
    path(r'video/', views.video, name='video'),

]
