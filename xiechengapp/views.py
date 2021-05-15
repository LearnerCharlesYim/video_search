from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from xiechengapp.models import xiechengItem, User
import uuid
from .spider import get_details
from .models import Video
import random
import json
from random import randrange
from django.http import HttpResponse
from rest_framework.views import APIView
from pyecharts.charts import Bar,Pie,Line
from pyecharts.faker import Faker
from pyecharts import options as opts
from django.db.models import Count

def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error

def pie_base(result):
    c = (
        Pie()
        .add("", result)
        .set_colors(["yellow", "red", "blue"])
        .set_global_opts(title_opts=opts.TitleOpts(title="格式与数量", subtitle="数据来自熊猫网"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .dump_options_with_quotes()
    )
    return c

def bar_base(result):
    c = (
        Bar()
        .add_xaxis(["vsp", "prproj", 'aep'])
        .add_yaxis("视频数量", result)
        .set_global_opts(title_opts=opts.TitleOpts(title="种类与大小", subtitle="数据来自熊猫网"))
        .dump_options_with_quotes()
    )
    return c

def line_base(ls):
    x_data = ["2000", "4000", "6000", "8000", "10000", "12000",'12000+']
    c = (
        Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="数量",
            stack="总量",
            y_axis = ls,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="热度", subtitle="数据来自熊猫网"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        .dump_options_with_quotes()

    )
    return c

class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        aep_count = Video.objects.filter(format='aep').aggregate(aep_num=Count('id'))['aep_num']
        prproj_count = Video.objects.filter(format='prproj').aggregate(prproj_num=Count('id'))['prproj_num']
        vsp_count = Video.objects.filter(format='vsp').aggregate(vsp_num=Count('id'))['vsp_num']
        result = [['vsp',vsp_count],['prproj',prproj_count],['aep',aep_count]]
        return JsonResponse(json.loads(pie_base(result)))

class ChartBarView(APIView):
    def get(self,request,*args,**kwargs):
        aep_count = Video.objects.filter(format='aep').aggregate(aep_num=Count('id'))['aep_num']
        prproj_count = Video.objects.filter(format='prproj').aggregate(prproj_num=Count('id'))['prproj_num']
        vsp_count = Video.objects.filter(format='vsp').aggregate(vsp_num=Count('id'))['vsp_num']
        result = [vsp_count,prproj_count,aep_count]
        return JsonResponse(json.loads(bar_base(result)))

class ChartLineView(APIView):
    def get(self,request,*args,**kwargs):
        ls2000 = [str(i) for i in range(0,2001)]
        ls4000 = [str(i) for i in range(2000,4001)]
        ls6000 = [str(i) for i in range(4000,6001)]
        ls8000 = [str(i) for i in range(6000,8001)]
        ls10000 = [str(i) for i in range(8000,10001)]
        ls12000 = [str(i) for i in range(10000,12001)]
        ls = [
            Video.objects.filter(heat__in=ls2000).aggregate(Count('id')).popitem()[1],
            Video.objects.filter(heat__in=ls4000).aggregate(Count('id')).popitem()[1],
            Video.objects.filter(heat__in=ls6000).aggregate(Count('id')).popitem()[1],
            Video.objects.filter(heat__in=ls8000).aggregate(Count('id')).popitem()[1],
            Video.objects.filter(heat__in=ls10000).aggregate(Count('id')).popitem()[1],
            Video.objects.filter(heat__in=ls12000).aggregate(Count('id')).popitem()[1],
            Video.objects.aggregate(Count('id')).popitem()[1]-Video.objects.filter(heat__in=ls2000).aggregate(Count('id')).popitem()[1]-Video.objects.filter(heat__in=ls4000).aggregate(Count('id')).popitem()[1]-Video.objects.filter(heat__in=ls6000).aggregate(Count('id')).popitem()[1]-Video.objects.filter(heat__in=ls8000).aggregate(Count('id')).popitem()[1]-Video.objects.filter(heat__in=ls10000).aggregate(Count('id')).popitem()[1]-Video.objects.filter(heat__in=ls12000).aggregate(Count('id')).popitem()[1],

        ]

        return JsonResponse(json.loads(line_base(ls)))

def index(request):
    utoken = request.COOKIES.get('utoken', None)
    if utoken:
        return render(request, '../templates/index.html', context={})
    else:
        return redirect(reverse('xiechengapp:login'))

def video(request):
    utoken = request.COOKIES.get('utoken', None)
    if utoken:
        if request.method == 'GET':
            kw = request.GET.get('kw','')
            if kw:
                videos = Video.objects.filter(name__contains=kw)
                return render(request,'videodetail.html',context={'videos':videos,'kw':kw})
            return render(request,'videodetail.html')

def search(request):
    utoken = request.COOKIES.get('utoken', None)
    if utoken:
        user = User.objects.filter(utoken=utoken).first()
        if request.method == 'GET':
            kw = request.GET.get('kw')
            videos = Video.objects.filter(name__contains=kw)

            return render(request, '../templates/index2.html', context={'videos':videos, 'kw':kw})
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

    video = Video.objects.get(id=video_id)
    return render(request,'video_d.html',context={'video':video})



