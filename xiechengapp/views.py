from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from xiechengapp.models import xiechengItem, User
import uuid
from .spider import get_details
from .models import Video
import random

def index(request):
    utoken = request.COOKIES.get('utoken', None)
    if utoken:
        return render(request, '../templates/index.html', context={})
    else:
        return redirect(reverse('xiechengapp:login'))

def serch(request):
    utoken = request.COOKIES.get('utoken', None)
    if utoken:
        user = User.objects.filter(utoken=utoken).first()
        if request.method == 'GET':
            kw = request.GET.get('kw')
            videos = Video.objects.filter(name__contains=kw)

            return render(request, '../templates/index.html', context={'videos':videos})
    else:
        return redirect(reverse('xiechengapp:login'))

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)
        upwd2 = request.POST.get('upwd2', None)
        user = User.objects.filter(uname=uname).first()
        if user:
            return redirect(reverse('xiechengapp:register'))
        if uname and upwd and upwd2 and upwd == upwd2:
            user = User()
            user.uname = uname
            user.upwd = upwd
            user.save()

            return login(request)
        else:
            return redirect(reverse('xiechengapp:register'))


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)

        if uname and upwd:
            user = User.objects.filter(uname=uname).first()
            if user and user.upwd == upwd:
                utoken = uuid.uuid4()
                resp = HttpResponseRedirect(reverse('xiechengapp:index'))
                user.utoken = utoken    #服务端token
                user.save()
                resp.set_cookie('utoken', utoken)       #前端token

                return resp
    return redirect(reverse('xiechengapp:login'))


def logout(request):
    resp = HttpResponseRedirect(reverse('xiechengapp:index'))
    resp.delete_cookie('utoken')
    return resp


def video_detail(request,video_id):
    print(video_id)
    video = Video.objects.get(id=video_id)
    return render(request,'video_detail.html',context={'video':video})



