from django.urls import path
from . import views
from .views import search_results, login_page, profile_page


urlpatterns = [
    path('', views.home, name="home"),
    path('groups/<str:pk>/', views.group, name="groups"),
    path('search/', search_results, name='search_results'),
    path('login/', login_page, name='login'),
    path('profile', profile_page, name='profile'),
]
