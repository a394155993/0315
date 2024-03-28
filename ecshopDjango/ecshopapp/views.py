from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from ecshopapp import models
from django.http import JsonResponse, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger
import markdown
# Create your views here.
def index(request):
    good_obj = models.Goods.objects.filter(status=1)
    context = {
        'new_goods_obj': good_obj.order_by('-add_datetime')[:5],
    }
    return render(request, 'ecshopapp/index.html', context)


#user logout

def acc_logout(request):
    logout(request)
    return redirect('/login')

def acc_login(request):
    if request.method == 'GET':
        return render(request, 'ecshopapp/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/'))
        else:
            return render(request,'ecshopapp/login.html',{'erro':"please check your username or password!"})
    
def acc_register(request):
    if request.method == 'GET':
        return render(request, 'ecshopapp/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        hash_reg_password = make_password(password2)
        first_name = request.POST.get('first_name')
        email = request.POST.get('user_email')
        if password1 != password2:
            return JsonResponse({"status": False, "error-tips":'Two passwords do not match!'})
        if models.User_Member.objects.filter(user_name=username).exists() or models.User_Member.objects.filter(user_email=email).exists():
            return JsonResponse({'status': False, 'error_tips': 'Username or email already exists!'})
        user = models.User_Member.objects.create(user_name=username, user_email=email, password=hash_reg_password,
                                                     user_nickname=first_name)
        login(request,user)
        return redirect('/')
                                     

def shop(request):
    goods_obj = models.Goods.objects.filter(status=1)
    search = request.GET.get('search')
    goods_type = request.GET.get('goods_type')
    publishings = request.GET.get('publishings')
    if search:
        goods_obj = goods_obj.filter(name__icontains=search)
    if goods_type:
        goods_obj = goods_obj.filter(goods_type=goods_type)
    if publishings:
        goods_obj = goods_obj.filter(publishings=publishings)
    goods_list = list(goods_obj.values('id','name', 'price', 'stock', 'image','goods_type', 'publishings'))
    context = {
        'goods_obj': goods_list,
    }
    return render(request, 'ecshopapp/shop_list.html', context)


@login_required
def detail(request, good_id):
    good_obj = get_object_or_404(models.Goods, pk=good_id)
    md_content = good_obj.content
    html_content = markdown.markdown(md_content)
    return render(request, 'ecshopapp/detail.html', {'good_obj': good_obj,'html_content': html_content})



# def goods_type(request):
#     good_type = models.Goods.objects.filter(status=1).values_list('goods_type', flat=True).distinct()
#     return good_type