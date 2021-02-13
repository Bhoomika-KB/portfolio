from django.urls import path
from . import views

urlpatterns = [
    path('', views.covid, name='covid')
]
