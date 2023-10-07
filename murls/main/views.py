from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegisterForm, AddProfile, AddBiogram, AddAvatar, CustomAuthenticationForm, TwoFactorAuthForm
from .models import ProfileLink, ProfileBiogram, Avatar, TwoFactorAuth
from .token import account_activation_token


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


@login_required(login_url='/login')
def settings(request):
    if request.method == 'POST':
        form = TwoFactorAuthForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)
            state.user = request.user
            form.save()

            return redirect("/settings")
    else:
        form = TwoFactorAuthForm()

    auth_state = TwoFactorAuth.objects.filter(user=request.user.id).last()

    context = dict(
        form=form,
        auth_state=auth_state
    )
    return render(request, 'main/settings.html', context=context)


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('registration/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'{user}, zaloguj się na swoją pocztę {to_email} i kliknij  otrzymany link '
                                  f'aktywacyjny, aby potwierdzić rejestrację. Jeżeli nie widzisz maila, '
                                  f'sprawdź folder spam lub inne.')
    else:
        messages.error(request, f'Problem podczas wysyłania maila na {to_email}. Sprawdź poprawność adresu e-mail')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Zweryfikowaliśmy Twój adres, teraz możesz się zalogować.')
        return redirect('/login')
    elif user.is_active == True:
        messages.error(request, 'Twoje konto zostało już wcześniej aktywowane.')
    else:
        messages.error(request, 'Błąd aktywacji')

    return redirect('/home')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))

            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})


...


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


def show_profile_page(request, username):
    try:
        user_login = User.objects.get(username=username)
        user_n = User.objects.filter(username=username).first()
        user_id = user_n.id
        user_links = ProfileLink.objects.filter(owner=user_id)
        user_bio = ProfileBiogram.objects.filter(owner_id=user_id).last()
        user_avatar = Avatar.objects.filter(user=user_id).last()

        context = dict(
            user_login=user_login,
            user_n=user_n,
            user_id=user_id,
            user_links=user_links,
            user_bio=user_bio,
            user_avatar=user_avatar
        )

        return render(request, 'main/user_profile.html', context=context)
    except ObjectDoesNotExist:
        return render(request, 'main/user_not_exist.html', {"username": username})
