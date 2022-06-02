import json
from datetime import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory, TblVideo, TblSettingWeb
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from .stwform import SettingForm
from django.core.paginator import Paginator
from Constant import SERVER_URL
# Create your views here.

def decode_Item_Setting(stw):
    stw['ads_key_banner'] = bs.decode_Str(stw['ads_key_banner'])
    stw['ads_key_interstial'] = bs.decode_Str(stw['ads_key_interstial'])
    stw['ad_display_count'] = int(stw['ad_display_count'])
    stw['ads_key_openads'] = bs.decode_Str(stw['ads_key_openads'])
    return stw

def decode_Item_Video(video):
    video['vid_id'] = int(video['vid_id'])
    video['cat_id'] = int(video['cat_id'])
    video['vid_title'] = bs.decode_Str(video['vid_title'])
    video['vid_url'] = bs.decode_Str(video['vid_url'])
    video['vid_thumbnail'] = bs.decode_Str(video['vid_thumbnail'])
    video['vid_description'] = bs.decode_Str(video['vid_description'])
    video['vid_view'] = int(video['vid_view'])
    video['vid_duration'] = int(video['vid_duration'])
    video['vid_avg_rate'] = float(video['vid_avg_rate'])
    video['vid_status'] = int(video['vid_status'])
    video['vid_type'] = int(video['vid_type'])
    video['vid_is_premium'] = int(video['vid_is_premium'])
    return video

def decode_Video(videos):
    for video in videos:
        video = decode_Item_Video(video)
    return videos

def getSettingweb():
    postObj = {
        'method_name': 'GET_SETTING',
    }

    data = {
        'data': json.dumps(postObj)
    }

    res = requests.post(SERVER_URL , data = data)
    return_obj = json.loads(res.content)

    return return_obj['setting_array'] if return_obj['status'] == "success" else []

def settingweb(request, able):
    settingweb = getSettingweb()
    settingweb = decode_Item_Setting(settingweb)
    context = {}
    
    context = {'able':able, 'settingweb':settingweb}
    return render(request, 'settingweb/settingweb.html', context)

def choiceTrending(request, type):
    settingweb = getSettingweb()
    if request.method == 'POST':
        list_trend = request.POST.getlist('list_trend')
        str_temp = 'RESULT'
        for i in list_trend:
            str_temp = str_temp + ':' + i

        postObj = {
            'method_name': 'UPDATE_ARR_TREND',
            'arr_trend':str_temp,
            'type':type
        }

        data = {
            'data': json.dumps(postObj)
        }

        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)
        if str(return_obj) == "success":
            return redirect('settingweb:setting', "1")
        else:
            return HttpResponse("Error")
    else:
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        list_trend = []
        if type == "1":
            list_trend = settingweb['arr_Vid_trend'].split(':')
        if type == "2":
            list_trend = settingweb['arr_TV_trend'].split(':')
        if type == "3":
            list_trend = settingweb['arr_Radi_trend'].split(':')
       
        postObj = {
            'method_name': 'LOAD_TV_OR_RADIO',
            'type':type,
            'cate_id': 0,
            'search_txt': q
        }

        data = {
            'data': json.dumps(postObj)
        }

        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)

        videos = return_obj['all'] if return_obj['status'] == "success" else []
        videos = decode_Video(videos)

        list_trend.pop(0)
        list_trend = [int(item) for item in list_trend]

        #Paginator
        p = Paginator(videos, 6)
        page = request.GET.get('page') 
        list_vid = p.get_page(page)
        nums = "a" * list_vid.paginator.num_pages

        context = {'type':type, 'videos':list_vid, 'list_trend':list_trend, 'nums': nums}
        return render(request, 'settingweb/choicetrend.html', context)

def updateSTW(request):
    settingweb = getSettingweb()
    settingweb = decode_Item_Setting(settingweb)
    if request.method == 'POST':
        postObj = {
            'method_name': 'UPDATE_SETTING',
            'ads_key_banner': bs.encode_Str(request.POST.get('banner')), 
            'ads_key_interstial':bs.encode_Str(request.POST.get('interstial')),
            'ad_display_count':request.POST.get('count'),
            'ads_key_openads': bs.encode_Str(request.POST.get('openads')), 
            'arr_Vid_trend': request.POST.get('vid_trend'),
            'arr_TV_trend':  request.POST.get('tv_trend'),
            'arr_Radi_trend':  request.POST.get('radio_trend')
        }

        data = {
            'data': json.dumps(postObj)
        }

        res = requests.post(SERVER_URL , data = data)
        return_obj = json.loads(res.content)
        if str(return_obj) == "success":
            return redirect('settingweb:setting', "0")
        else:
            return HttpResponse("Error")
    else:
        return HttpResponse("Error")