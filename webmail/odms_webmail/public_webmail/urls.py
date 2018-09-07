from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mails/', views.mails_no_domain, name='mails'),
    path('mails/<str:email_domain>/', views.mails_no_address, name='mails'),
    path('mails/<str:email_domain>/<str:email_address>/', views.mails, name='mails'),
]