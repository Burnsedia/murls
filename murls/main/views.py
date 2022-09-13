from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, AddProfile, AddBiogram, AddAvatar, CustomAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ProfileLink, ProfileBiogram, Avatar
from django.http import HttpResponse

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
def my_custom_page_not_found_view(request, exception):
    return render(request, "main/errors/404.html", {})

def landing(request):
    return render(request, 'main/landing.html')

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

@login_required(login_url='/login')
def add_biogram(request):
    initial_dict = {
        "biogram": ProfileBiogram.objects.filter(owner_id=request.user.id).last()
    }

    if request.method == 'POST':
        form = AddBiogram(request.POST or None, request.FILES, initial=initial_dict)
        if form.is_valid():
            link = form.save(commit=False)
            link.owner = request.user
            link.save()

            return redirect("/home")
    else:
        form = AddBiogram(initial=initial_dict)

    return render(request, 'main/biogram.html', {"form": form})

def add_avatar(request):
    user_avatar = Avatar.objects.filter(user=request.user.id).last()
    if request.method == 'POST':
        form = AddAvatar(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("/add-avatar")
    else:
        form = AddAvatar()

    return render(request, 'main/avatar.html', {"form": form, "user_avatar": user_avatar})

def ShowProfilePage(request, username):
        user_login = User.objects.get(username=username)
        user_n = User.objects.filter(username=username).first()
        user_id = user_n.id
        user_links = ProfileLink.objects.filter(owner=user_id)
        user_bio = ProfileBiogram.objects.filter(owner_id=user_id).last()
        user_avatar = Avatar.objects.filter(user=user_id).last()

        return render(request, 'main/user_profile.html', {"user_login": user_login, "user_links": user_links,
                                                          "user_bio": user_bio, "user_avatar": user_avatar})
