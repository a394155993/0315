from django.urls import path, include, re_path
from ecshopapp import views
from django.contrib import admin
from ecshop.settings import MEDIA_ROOT
from django.views.static import serve


urlpatterns = [
    path('', views.index, name='index'),  # homepage
    path('logout', views.acc_logout, name='logout'),#logout
    path('login', views.acc_login, name='login'),#login
    path('register', views.acc_register, name='register'),#register
    path('Shop', views.shop, name='shop'),  # shop
    path('detail/<int:good_id>', views.detail, name='detail'), #detail
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    
]