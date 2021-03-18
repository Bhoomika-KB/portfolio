from django.urls import path
from . import views


urlpatterns = [
   path('', views.homepage, name='homepage'),
   path('<int:id>/', views.single_class, name='single_class'),
   path('login/', views.login, name='login'),
   path('logout/', views.logout, name='logout'),
   path('register/<str:class_name>/', views.register, name='register'),
   path('profile/', views.profile, name='profile'),
   path('about_page/', views.about_page, name='about_page')

]
