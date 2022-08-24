from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signup', views.sign_up, name='signup'),
    path('add-profile', views.add_link, name='addlink'),
    path('add-biogram', views.add_biogram, name='biogram'),
    path('@<str:username>/', views.ShowProfilePage, name='ShowProfilePage'),
]


