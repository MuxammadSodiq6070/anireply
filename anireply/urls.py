from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('animelar/', views.animelar_page, name='animelar'),    
    path('home/', views.home_page, name='home_page'),    
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_page, name="logout"),
    path("anime/<int:pk>/episode/<int:episode_number>/", views.anime_detail, name="anime_episode"),
    path("anime/<int:pk>/", views.anime_detail, name="anime_detail"),
]
