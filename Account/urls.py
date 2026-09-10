from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'profile'

urlpatterns = [
    path('', views.profile_index, name='profile_index'),
    path('edit/', views.edit_profile, name='profile_edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logedout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/password', views.password_change, name='password_change'),
    path('following/<str:username>/', views.following, name='following'),]
