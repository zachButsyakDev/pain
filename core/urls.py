from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('study-session/close/', views.close_study_session, name='close_study_session'),
]