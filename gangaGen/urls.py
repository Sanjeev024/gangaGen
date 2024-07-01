from django.contrib import admin
from django.urls import path, include
from gangaGen import views

urlpatterns = [
    path('', views.home, name='home'),
    path('database/', views.database, name='database'),
    path('search_sequence/', views.search_sequence, name='search_sequence'),
    path('user-login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name="logout_view"),
    path('search_proteins/', views.search_proteins, name='search_proteins'),
    path('search_seq/', views.search_seq, name='search_seq'),
   
]
