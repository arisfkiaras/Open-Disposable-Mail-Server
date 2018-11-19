from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Email lists
    path('mails/', views.all_emails, name='mails'),
    path('mails/<str:domain>/', views.domain_emails, name='mails'),
    path('mails/<str:domain>/<str:username>/', views.full_address_emails, name='mails'),
    
    # Specific Email
    path('mail/<str:id>/', views.email_by_id, name='email_by_id'),

]