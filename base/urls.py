from django.urls import path
from . import views
from .views import search_results, login_page, profile_page


urlpatterns = [
    path('', views.home, name="home"),
    path('groups/<str:pk>/', views.group, name="groups"),
    path('search/', search_results, name='search_results'),
    path('login/', views.login_page, name='login'),
    path('profile', profile_page, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/create/<int:group_id>/', views.create_post, name='create_group_post'),
    
]
