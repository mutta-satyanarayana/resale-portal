from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
app_name = 'users'
#from django.contrib.auth import views as v

# Define Your urls Here

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('remove/', views.removeuser, name = 'removeuser'),
    path('profile',views.profile, name = 'profile'),
    path('editprofile',views.editprofile, name = 'editprofile'),
    path('login/',LoginView.as_view(template_name="users/login.html"),name="login"),
    path('logout/',views.logout,name="logout"),
	#path('logout/',LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    #path('update/<int:id>/', views.update, name = 'update'),
    #path('info/', views.info, name = 'info'),

]