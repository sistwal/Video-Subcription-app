from django.urls import path
from . import views

urlpatterns = [
   path('',views.home, name="home"),
   path('video/<slug>/',views.view_video, name="video"),
   path('become_pro/',views.become_pro, name="become_pro"),
   path('charge/',views.charge, name="charge"),
   path('login/',views.login_attempt, name="login_attempt"),
   path('register/',views.sign, name="register_attempt"),
   path('logout/',views.logout_attempt, name="logout_attempt"),
   path('about/', views.about, name="about"),
   path('contact', views.contact, name="contact"),
   path('detail/', views.detail, name="detail"),
   path('edit/', views.edit, name="edit"),
]