from django.urls import path
from basicApp import views

app_name = 'basicApp'

urlpatterns = [
    path('', views.index,name='index'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='logout'),
    path('special/', views.special,name='special'),
]
