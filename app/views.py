from django.shortcuts import render,redirect
from . models import *
import stripe
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models.query import *

def home(request):
 videos = Video.objects.all()
 if request.user.is_authenticated:
   request.session
   curr_user = request.user.id
   is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
   context = {'videos': videos, 'is_pro': str(is_pro)}
   return render(request, 'home.html',context)

 context = {'videos': videos}
 return render(request, 'home.html',context)


def view_video(request,slug):
  if request.user.is_authenticated:
    curr_user = request.user.id
    is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
    if str(is_pro) == "<QuerySet [{'is_pro': True}]>":
      videos = Video.objects.filter(slug = slug)
      context = {'videos': videos, 'is_pro':str(is_pro)}
      return render(request,'video.html',context)
    else:
      is_premium = Video.objects.filter(slug = slug).values('is_Premium') 
      if str(is_premium) == "<QuerySet [{'is_Premium': False}]>":
        videos = Video.objects.filter(slug = slug)
        context = {'videos': videos, 'is_pro':str(is_pro)}
        return render(request, 'video.html', context)
      else:
        context = {'message':'You have to Buy Premium then you can Enjoy! Till Then you can enjoy Free Series', 'is_pro':str(is_pro) }
        return render(request, 'video.html', context)
  else:
   context = {'message':'You have to Login First!'}
   return render(request, 'video.html', context)

def charge(request):
 if request.user.is_authenticated:
   curr_user = request.user.id
   is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
   context = {'is_pro':str(is_pro)}
   return render(request, 'charge.html', context)
 else:
   context = {'message': 'You have to login first!'}
   return render(request, 'charge.html', context)

def sign(request):
 if request.method == 'POST':
   username = request.POST.get('username')
   email = request.POST.get('email')
   password = request.POST.get('Password')
   user = User(username=username, password=password, email=email)
   
   if user is None:
    context = {'message': 'Fill again!'}
    return render(request,'register.html', context)
   else:
    if User.objects.filter(username=username).count():
      context = {'message': 'User already registered'}
      return render(request,'register.html', context)
    else:
      user = User(username=username, email=email)
      user.set_password(password)
      user.save()
      context = {'message': 'User registered'}
      return render(request, 'register.html', context)
 curr_user = request.user.id 
 is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
 context = {'is_pro':str(is_pro)}
 return render(request, 'register.html',context)

def login_attempt(request):
 if request.method == 'POST':
   form = AuthenticationForm(request=request.POST, data= request.POST)
   if form.is_valid():
     username = request.POST.get('username','')
     password = request.POST.get('password','')
     user = authenticate(username=username, password=password)
     login(request, user)
     return redirect("/")
 else:
   form = AuthenticationForm()
 curr_user = request.user.id 
 is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
 context = {'form':form, 'is_pro':str(is_pro)}
 return render(request, 'login.html',context)


def logout_attempt(request):
  logout(request)
  return redirect('/')


def become_pro(request):
 
 if request.method == 'POST':
  membership = request.POST.get('membership')
  if membership == 'MONTHLY':
    amount = 100000
  elif membership == 'YEARLY':
    amount = 1000000
  else:
    message = {'message':'Fill Correctly!'}
    return render(request, 'become_pro.html', message)
  stripe.api_key = "sk_test_51JURDhSHIJ8I9fLuIgLLjoMyzKH7yiWohi6EIgGKlD8VjiZKKcChaKvduIAWRvaoOtZkTqUqhzyH7iq2oIrSmGMv00h4sLiUVH"

  customer = stripe.Customer.create(
    api_key = "sk_test_51JURDhSHIJ8I9fLuIgLLjoMyzKH7yiWohi6EIgGKlD8VjiZKKcChaKvduIAWRvaoOtZkTqUqhzyH7iq2oIrSmGMv00h4sLiUVH",
    email = request.user.email,
    source="tok_visa"
  )

  charge = stripe.Charge.create(
    api_key="sk_test_51JURDhSHIJ8I9fLuIgLLjoMyzKH7yiWohi6EIgGKlD8VjiZKKcChaKvduIAWRvaoOtZkTqUqhzyH7iq2oIrSmGMv00h4sLiUVH",
    customer = customer,
    amount = amount,
    currency = 'inr',
    description = "membership"
  ) 
  if charge['paid'] == True:
   profile = Profile(user = request.user)
   if charge['amount'] == 100000:
    profile.subscription_type = 'M'
    profile.is_pro = True
    expiry = datetime.now() + timedelta(30)
    profile.pro_expiery_date = expiry
    profile.save()
   elif charge['amount'] == 1000000:
    profile.subscription_type = 'Y'
    profile.is_pro = True
    expiry = datetime.now() + timedelta(365)
    profile.pro_expiery_date = expiry
    profile.save()
   curr_user = request.user.id
   is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
   context = {'is_pro':str(is_pro)}
   return render(request, 'charge.html',context)
 curr_user = request.user.id 
 is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
 context = {'is_pro':str(is_pro)}
 return render(request,'become_pro.html', context)

def contact(request):
  if request.method == 'POST':
   name = request.POST.get('name')
   email = request.POST.get('email')
   phone = request.POST.get('phone')
   desc = request.POST.get('desc')
   contact = Contact(name=name, email=email,phone=phone, desc=desc)
   contact.save()
  curr_user = request.user.id 
  is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
  context = {'is_pro':str(is_pro)}
  return render(request, 'contact.html',context)

def about(request):
  curr_user = request.user.id 
  is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
  context = {'is_pro':str(is_pro)}
  return render(request, 'about.html',context)

def detail(request):
 curr_user = request.user.id
 exist = Profile.objects.filter(user = curr_user).exists()
 if exist:
  curr_user = request.user.id 
  is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
  
  pro_expiery_date = Profile.objects.filter(user = curr_user).values('pro_expiery_date')
  expiry = pro_expiery_date[0]['pro_expiery_date']
  
  prem = Profile.objects.filter(user = curr_user).values('subscription_type')
  premium = prem[0]['subscription_type']
  
  context = {'is_pro':str(is_pro), 'premium': premium, 'expiry':expiry}
  return render(request, 'detail.html', context)
 else:
  curr_user = request.user.id 
  is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
  premium = 'F'
  expiry = 'You are not a pro member'
  context = {'is_pro':str(is_pro), 'premium': premium, 'expiry':expiry}
  return render(request, 'detail.html', context)

def edit(request):
  if request.method == 'POST':
   email = request.POST.get('email')
   curr_user = request.user.id
   User.objects.filter(id = curr_user).update(email=email)
   is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
   context = {'message': 'Your Email is Updated','is_pro':str(is_pro)}
   return redirect("/edit")

  curr_user = request.user.id
  is_pro = Profile.objects.filter(user = curr_user).values('is_pro')
  context={'is_pro':str(is_pro)}
  return render(request, 'edit.html', context)