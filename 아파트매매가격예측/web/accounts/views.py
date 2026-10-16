import os
from django.shortcuts import render, redirect
from .models import User, Predict
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm
from django.http.request import HttpRequest
from joblib import load
import pandas as pd

def home(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk = user_id)
        return HttpResponse("Hello! %s님" % user)
    else:
        return render(request, 'index.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None) 
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        
        err_data={}
        if not(username and useremail and password and re_password):
            err_data['error'] = '모든 값을 입력해주세요.'
            return render(request, 'register.html', err_data)
        
        elif password != re_password:
            err_data['error'] = '비밀번호가 다릅니다.'
            return render(request, 'register.html', err_data)
        
        else:
            user = User(
                username=username,
                useremail=useremail,
                password=make_password(password),
            )
            user.save()
            return redirect('/')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')


def predict(request:HttpRequest, *args, **kwargs):
    if request.method == "POST":
        predict = Predict()
        predict.first = request.POST['first']
        predict.second = request.POST['second']
        predict.third = request.POST['third']
        predict.fourth = request.POST['fourth']

        model = load(os.path.join(os.path.dirname(__file__), 'house.joblib'))

        input_variables = pd.DataFrame([[predict.first, predict.second, predict.third, predict.fourth]],
                        columns=['금리', '국내총생산', '대출금리', '아파트거래량'],
                        dtype='float',
                        index=['input'])

        prediction = model.predict(input_variables)[0]

        context = {
        "first" : predict.first,
        "second" : predict.second,
        "third" : predict.third,
        "fourth" : predict.fourth,
        "prediction" : prediction
        }

        return render(request, 'index.html', context=context)
    
    return render(request, 'index.html')