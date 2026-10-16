from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path('', views.board_main, name='board_main'),
    path('test', views.test, name="test"),
    path('apart', views.apart, name="apart"),
    path('lda_21_1', views.lda_21_1, name="lda_21_1"),
    path('lda_21_2', views.lda_21_2, name="lda_21_2"),
    path('lda_21_3', views.lda_21_3, name="lda_21_3"),
    path('lda_21_4', views.lda_21_4, name="lda_21_4"),
    path('lda_21_5', views.lda_21_5, name="lda_21_5"),
    path('lda_21_6', views.lda_21_6, name="lda_21_6"),
    path('lda_21_7', views.lda_21_7, name="lda_21_7"),
    path('lda_21_8', views.lda_21_8, name="lda_21_8"),
    path('lda_21_9', views.lda_21_9, name="lda_21_9"),
    path('lda_21_10', views.lda_21_10, name="lda_21_10"),
    path('lda_21_11', views.lda_21_11, name="lda_21_11"),
    path('lda_21_12', views.lda_21_12, name="lda_21_12"),
    path('lda_22_1', views.lda_22_1, name="lda_22_1"),
    path('lda_22_2', views.lda_22_2, name="lda_22_2"),
    path('lda_22_3', views.lda_22_3, name="lda_22_3"),
    path('lda_22_4', views.lda_22_4, name="lda_22_4"),
    path('lda_22_5', views.lda_22_5, name="lda_22_5"),
    path('lda_22_6', views.lda_22_6, name="lda_22_6"),
    path('lda_22_7', views.lda_22_7, name="lda_22_7"),
    path('lda_22_8', views.lda_22_8, name="lda_22_8"),
    path('lda_22_9', views.lda_22_9, name="lda_22_9"),
    path('lda_22_10', views.lda_22_10, name="lda_22_10"),
    path('lda_22_11', views.lda_22_11, name="lda_22_11"),
    path('lda_22_12', views.lda_22_12, name="lda_22_12"),
    path('아파트실거래가_1분위', views.map1, name="아파트실거래가_1분위"),
    path('아파트실거래가_2분위', views.map2, name="아파트실거래가_2분위"),
    path('아파트실거래가_3분위', views.map3, name="아파트실거래가_3분위"),
    path('아파트실거래가_4분위', views.map4, name="아파트실거래가_4분위")
]