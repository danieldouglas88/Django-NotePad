from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from .models import NotePad
import datetime
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required
def index (request):
    currenttime = datetime.datetime.now()
    user = request.user.username
    last_login = User.objects.get(username=user).last_login
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