from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.landing, name='landing'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('home', views.home, name='home'),
    path('signup', views.sign_up, name='signup'),
    path('add-profile', views.add_link, name='addlink'),
    path('add-biogram', views.add_biogram, name='biogram'),
    path('add-avatar', views.add_avatar, name='avatar'),
    path('@<str:username>/', views.show_profile_page, name='ShowProfilePage'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]


