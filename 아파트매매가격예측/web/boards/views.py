from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .models import Board, Predict
from .forms import BoardForm
from accounts.models import User
from django.core.paginator import Paginator
# from .models import Tag
#from tag.models import Tag
from django.http.request import HttpRequest
import pandas as pd
from joblib import load
import joblib
import tarfile
import pickle

def board_main(request):
    redirect('/')

def test(request):
    return render(request, 'test.html')

def apart(request):
    return render(request, 'apart.html')

def map1(request):
    return render(request, '아파트실거래가_1분위.html')

def map2(request):
    return render(request, '아파트실거래가_2분위.html')

def map3(request):
    return render(request, '아파트실거래가_3분위.html')

def map4(request):
    return render(request, '아파트실거래가_4분위.html')

def lda_21_1(request):
    return render(request, 'lda/lda_21_1.html') 

def lda_21_2(request):
    return render(request, 'lda/lda_21_2.html') 

def lda_21_3(request):
    return render(request, 'lda/lda_21_3.html') 

def lda_21_4(request):
    return render(request, 'lda/lda_21_4.html') 

def lda_21_5(request):
    return render(request, 'lda/lda_21_5.html') 

def lda_21_6(request):
    return render(request, 'lda/lda_21_6.html')    

def lda_21_7(request):
    return render(request, 'lda/lda_21_7.html') 

def lda_21_8(request):
    return render(request, 'lda/lda_21_8.html') 

def lda_21_9(request):
    return render(request, 'lda/lda_21_9.html') 

def lda_21_10(request):
    return render(request, 'lda/lda_21_10.html') 

def lda_21_11(request):
    return render(request, 'lda/lda_21_11.html') 

def lda_21_12(request):
    return render(request, 'lda/lda_21_12.html') 

def lda_22_1(request):
    return render(request, 'lda/lda_22_1.html') 

def lda_22_2(request):
    return render(request, 'lda/lda_22_2.html')

def lda_22_3(request):
    return render(request, 'lda/lda_22_3.html')

def lda_22_4(request):
    return render(request, 'lda/lda_22_4.html')

def lda_22_5(request):
    return render(request, 'lda/lda_22_5.html')

def lda_22_6(request):
    return render(request, 'lda/lda_22_6.html')

def lda_22_7(request):
    return render(request, 'lda/lda_22_7.html')

def lda_22_8(request):
    return render(request, 'lda/lda_22_8.html')

def lda_22_9(request):
    return render(request, 'lda/lda_22_9.html')

def lda_22_10(request):
    return render(request, 'lda/lda_22_10.html')

def lda_22_11(request):
    return render(request, 'lda/lda_22_11.html')

def lda_22_12(request):
    return render(request, 'lda/lda_22_12.html')           


def predict(request:HttpRequest, *args, **kwargs):
    if request.method == "POST":
        predict = Predict()
        predict.first = request.POST['first']
        predict.second = request.POST['second']
        predict.third = request.POST['third']
        predict.fourth = request.POST['fourth']

        model = load('boards\house.joblib')

        input_variables = pd.DataFrame([[predict.first, predict.second, predict.third, predict.fourth]],
                        columns=['금리', '국내총생산', '대출금리', '매매 거래량'],
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

        return render(request, 'predict.html', context=context)
    
    return render(request, 'predict.html')