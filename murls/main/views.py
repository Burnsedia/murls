from django.shortcuts import render, redirect
from .forms import RegisterForm, AddProfile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ProfileLink


# Create your views here.

def home(request):
    links = ProfileLink.objects.filter(owner=request.user.id)

    if request.method == 'POST':
        link_id = request.POST.get("link-id")
        link = ProfileLink.objects.filter(id=link_id).first()

        if link and link.owner == request.user:
            link.delete()

    return render(request, 'main/home.html', {"links": links})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})


@login_required(login_url='/login')
def add_link(request):
    if request.method == 'POST':
        form = AddProfile(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.owner = request.user
            link.save()
            return redirect("/home")
    else:
        form = AddProfile()

    return render(request, 'main/add_profile.html', {"form": form})


def ShowProfilePage(request, username):
        user_login = User.objects.get(username=username)
        user_n = User.objects.filter(username=username).first()
        user_id = user_n.id
        user_links = ProfileLink.objects.filter(owner=user_id)
        return render(request, 'main/user_profile.html', {"user_login": user_login, "user_links": user_links})
