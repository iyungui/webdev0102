from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import dbUtils
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    context ={"user_id":request.session.get('user_id', '')}
    return render(request, "index.html", context)

import time
def login_view(request):
    curr_time = str(time.time()).split('.')[0]
    context ={'curr_time':curr_time}
    return render(request, "login.html", context)

@login_required
def my_info(request):
    context = {'url':request.session['user_img'] or 'static/assets/img/contact-bg.jpg'}
    return render(request, "my_info.html", context)

def get_result(status:bool, msg: str=''):
    if status:
        return {'rslt_cd':'0000', 'rslt_msg': msg}
    else:
        return {'rslt_cd':'1111', 'rslt_msg': msg}

def to_response(dict_data:dict):
    return JsonResponse(dict_data)

def error_view_500(request, exception):
    return render(request, "500.html", {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('login')

def login_req(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id", "")
        user_pw = request.POST.get('user_pw', "")
        rows = dbUtils.get_user(user_id, user_pw)

        if len(rows) == 0:
            return to_response(get_result(False, '등록되지 않은 사용자이거나, 비밀번호가 일치하지 않습니다.'))

        request.session['user_id'] = user_id
        request.session['user_nm'] = rows[0]['user_nm']
        request.session['user_img'] = rows[0]['user_img']

        user = User.objects.get(username=user_id)
        print('user', user)
        if user is None:
            user = User.objects.create_user(user_id)
        login(request, user)

        return to_response(get_result(True, rows[0]["user_nm"]))
    else:
        return tp_response(get_result(False))


@login_required
def upload_profile_img(request):
    if request.method == "POST":
        img_file = request.FILES.get('file1')

        if img_file is None:
            return to_response(get_result(False))

        fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
        filename = fs.save(img_file.name, img_file)
        uploaded_url = fs.url(filename)

        dbUtils.upd_user_img(request.session['user_id'], uploaded_url)
        request.session['user_img'] = uploaded_url

        return to_response(get_result(True, uploaded_url))
    else:
        return tp_response(get_result(False))

