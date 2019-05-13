from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('/notes', views.seenotes, name='seenotes'),
    path('/seemynotes', views.seemynotes, name='seemynotes'),
    path('login', views.login, name='login'),
    path('loginmessage', views.loginmessage, name='loginmessage'),
    path('logoutmessage', views.logoutmessage, name='logoutmessage'),
    path('createnote', views.createnote, name='createnote'),
]