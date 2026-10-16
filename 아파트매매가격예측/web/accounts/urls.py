from django.urls import path, include
from .views import home, predict, register, login, logout

app_name = "accounts"

urlpatterns = [
    path('', home, name='home'),
    path('predict/', predict, name='predict'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('boards/', include('boards.urls')),
]