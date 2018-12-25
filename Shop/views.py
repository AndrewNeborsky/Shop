from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from  django.shortcuts import redirect
from .models import *
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'currency': product.currency.code,
        })

    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        username = None

    context = {
        'products': data,
        'username': username
               }

    return render(request, 'index.html', context)


def log_out(request):
    logout(request)
    return redirect('index')


def log_in(request):
    user: User = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return render(request, 'login.html')

    login(request, user)
    return redirect('index')


def register(request):
    user: User = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username, password=password)
        user.save()
    except Exception as exc:
        print(exc, type(exc))
        return render(request, 'register.html')

    login(request, user)
    return redirect('index')


def products(request, product_id):
    product = Product.objects.get(id=product_id)

    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        username = None

    context = {
        'product': {'title': product.title, 'price': product.price, 'description': product.description,
                    'currency': product.currency.code},

        'username': username
    }

    return render(request, 'product.html', context)
