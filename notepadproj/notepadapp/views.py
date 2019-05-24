from django.contrib.auth.models import User
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from .models import NotePad
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urllib import parse


# Create your views here.
@login_required
def index (request):
    try:
        currenttime = datetime.datetime.now()
        last_login = User.objects.get(username=request.user.username).last_login
        return render(request, 'np/index.html', {"currenttime": currenttime, "last_login": last_login})
    except:
        return render(request, 'np/error.html')
    
@login_required
def seenotes (request):
    try:
        notes = NotePad.objects.all()
        return render(request, 'np/seenotes.html', {"notes": notes})
    except:
        return render(request, 'np/error.html')
    
@login_required
def seemynotes (request):
    try:
        notes = NotePad.objects.filter(username = request.user.username)
        return render(request, 'np/seemynotes.html', {"notes": notes})
    except:
        return render(request, 'np/error.html')
    
@login_required
def login(request):
    try:
        return render(request, 'np/loginmessage.html')
    except:
        return render(request, 'np/error.html')
    
def loginmessage(request):
    try:
        user = request.user.username
        return render(request, 'np/loginmessage.html', {"user":user})
    except:
        return render(request, 'np/error.html')
    
@login_required
def logoutmessage(request):
    try:
        user = request.user.username
        logout(request)
        return render(request, 'np/logoutmessage.html',  {"user":user})
    except:
        return render(request, 'np/error.html')
    
@login_required
def createnote(request):
    try:
        return render(request, 'np/createnote.html')
    except:
        return render(request, 'np/error.html')

@login_required
def search(request):
    try:
        unames = NotePad.objects.values('username').distinct()
        return render(request, 'np/search.html', {'unames': unames})
    except:
        return render(request, 'np/error.html')
    
def searchresult(request):
    try:
        searchterm = request.GET.get('searchterm')
        term = NotePad.objects.filter(username = searchterm)
        return render(request, 'np/searchresult.html', {'searchlist': term})
    except:
        return render(request, 'np/error.html')

def notedetails(request):
    try:
        notes = NotePad.objects.filter(id = request.GET.get('k'))
        return render(request, 'np/notedetails.html', {'notes': notes})
    except:
        return render(request, 'np/error.html')    
    
def notedelete(request):
    try:
        with connection.cursor() as cursor:
            nt = cursor.execute("DELETE FROM NotePad WHERE ID = '{0}'".format(request.GET.get('k')))
            return render(request, 'np/notedelete.html', {'nt': nt})
    except:
        return render(request, 'np/error.html')

@login_required        
def stats(request):
    try:
        stat = NotePad.objects.filter(username = request.user.username).count()
        updatenum = NotePad.objects.filter(username = request.user.username, update_date = None).count()
        teamnotes = NotePad.objects.filter().count()
        updatednotes = stat - updatenum
        updatepercent = (updatednotes/teamnotes) * 100
        userinfo = User.objects.get(username=request.user.username)
        divide = (stat/teamnotes) * 100
        longestcomment = NotePad.objects.raw("select id, length(comment), initialdate, comment from notepad where username = '{0}' order by length desc limit 1".format(request.user.username))
        if(str(stat) == '0'):
            return HttpResponse("Sorry, there are no stats for you yet. Please make at least 1 note in order to see your stats.")       
        else:
            return render(request, 'np/stats.html', {'stat': stat, 'teamnotes': teamnotes, 'divide': divide, 'userinfo':userinfo, 'longestcomment': longestcomment, 'updatednotes': updatednotes, 'updatepercent': updatepercent})
    except:
        return render(request, 'np/error.html')


def noteupdate(request):
    try:
        noteid = NotePad.objects.filter(id = request.GET.get('k'))
        return render(request, 'np/noteupdate.html', {"noteid":noteid})
    except:
        return render(request, 'np/error.html')

def updatesuccess(request):
    try:
        qs = parse.parse_qs(parse.urlparse(request.META.get('HTTP_REFERER')).query)['k'][0]
        update = NotePad.objects.filter(id=qs).update(comment = request.GET.get('commentbox'), update_date = datetime.datetime.now())
        return render(request, 'np/updatesuccess.html')
    except:
        return render(request, 'np/error.html')

def createsuccess(request):
    try:
        create = NotePad.objects.create()
        create.comment = request.GET.get('commentbox')
        create.initialdate = datetime.datetime.now()
        create.username = request.user.username
        create.save()
        return render(request, 'np/createsuccess.html', {"create": create})
    except:
        return render(request, 'np/error.html')
    
def error(request):
    return render(request, 'np/error.html')