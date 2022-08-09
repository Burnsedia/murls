from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signup', views.sign_up, name='signup'),
    path('add-profile', views.add_link, name='addlink'),
    # path('<str:username>/', views.user_profile, name='user_profile'),
]
