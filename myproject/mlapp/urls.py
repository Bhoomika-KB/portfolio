from django.urls import path,include
from rest_framework import routers
from .views import UserRegistraion,CarPrediction

router = routers.DefaultRouter()
router.register(r'users', UserRegistraion)



urlpatterns=[
    
    path('', include(router.urls)),
    path('predict/',CarPrediction.as_view(), name='car_price_prediction'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]