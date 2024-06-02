from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('signup', views.signup, name="signup"),
  path('signin', views.signin, name="signin"),
  path('signout', views.signout, name="signout"),
  path('history', views.history, name="history"),
  path('settings', views.settings, name="settings"),
  path('community', views.community, name="community"),
  path('homepage', views.homepage, name="homepage"),
  #path('result', views.result, name="result"),
  path('verify', views.predict_news, name="verify"),
]