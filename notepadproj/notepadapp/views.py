from django.contrib.auth.models import User
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from .models import NotePad
import datetime
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urllib import parse


# Create your views here.
@login_required
def index (request):
    currenttime = datetime.datetime.now()
    last_login = User.objects.get(username=request.user.username).last_login
    return render(request, 'np/index.html', {"currenttime": currenttime, "last_login": last_login})

@login_required
def seenotes (request):
    notes = NotePad.objects.all()
    return render(request, 'np/seenotes.html', {"notes": notes})

@login_required
def seemynotes (request):
    notes = NotePad.objects.raw("SELECT * FROM NotePad WHERE username = '{0}'".format(request.user.username))
    return render(request, 'np/seemynotes.html', {"notes": notes})

@login_required
def login(request):
    return render(request, 'np/loginmessage.html')

def loginmessage(request):
    user = request.user.username
    return render(request, 'np/loginmessage.html', {"user":user})

@login_required
def logoutmessage(request):
    user = request.user.username
    logout(request)
    return render(request, 'np/logoutmessage.html',  {"user":user})

@login_required
def createnote(request):
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit = True)
            post.save()
            form = NoteForm()
    else:
        form = NoteForm()
    return render(request, 'np/createnote.html', {'form': form})

@login_required
def search(request):
    unames = NotePad.objects.values('username').distinct()
    return render(request, 'np/search.html', {'unames': unames})

def searchresult(request):
    term = NotePad.objects.all()
    searchterm = request.GET.get('searchterm')
    term = NotePad.objects.raw("SELECT * FROM NotePad WHERE username = '{0}'".format(searchterm))
    return render(request, 'np/searchresult.html', {'searchlist': term})

def notedetails(request):
    try:
        notes = NotePad.objects.raw("SELECT * FROM NotePad WHERE ID = '{0}'".format(request.GET.get('k')))
        return render(request, 'np/notedetails.html', {'notes': notes})
    except:
        return HttpResponse("Sorry, there appears to be an issue")
    
def notedelete(request):
        with connection.cursor() as cursor:
            nt = cursor.execute("DELETE FROM NotePad WHERE ID = '{0}'".format(request.GET.get('k')))
            return render(request, 'np/notedelete.html', {'nt': nt})

@login_required        
def stats(request):
    stat = NotePad.objects.filter(username = request.user.username).count()
    updatenum = NotePad.objects.filter(username = request.user.username, update_date = None).count()
    teamnotes = NotePad.objects.filter().count()
    updatednotes = stat - updatenum
    updatepercent = (updatednotes/teamnotes) * 100
    userinfo = User.objects.get(username=request.user.username)
    divide = (stat/teamnotes) * 100
    longestcomment = NotePad.objects.raw("select id, length(comment), initialdate, comment from notepad where username = '{0}' order by length desc limit 1".format(request.user.username))
    if(str(stat) == '0'):
        return HttpResponse("Sorry, there are no stats for you yet.")       
    else:
        return render(request, 'np/stats.html', {'stat': stat, 'teamnotes': teamnotes, 'divide': divide, 'userinfo':userinfo, 'longestcomment': longestcomment, 'updatednotes': updatednotes, 'updatepercent': updatepercent})


def noteupdate(request):
    noteid = NotePad.objects.raw("SELECT * FROM NotePad WHERE ID = '{0}'".format(request.GET.get('k')))
    return render(request, 'np/noteupdate.html', {"noteid":noteid})

def updatesuccess(request):
    qs = parse.parse_qs(parse.urlparse(request.META.get('HTTP_REFERER')).query)['k'][0]
    update = NotePad.objects.filter(id=qs).update(comment = request.GET.get('commentbox'), update_date = datetime.datetime.now())
    return render(request, 'np/updatesuccess.html')

def createsuccess(request):
    create = NotePad.objects.create()
    create.comment = request.GET.get('commentbox')
    create.initialdate = datetime.datetime.now()
    create.username = request.user.username
    create.save()
    return render(request, 'np/createsuccess.html', {"create": create})