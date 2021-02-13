from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
import numpy as np



model = pickle.load(open('mlapp/random_forest_regression_model.pkl', 'rb'))




# Class BASED VIEW
class UserRegistraion(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
    
    
    


class CarPrediction(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        data = {
            'message':'You have to post the data inorder to predict the car price',
            
            'post_data':{
                "Year": "Integer Vlaue (2019, 2015 etc..)",
                "Present_Price": "Integer Vlaue in lakhs (2.5, 7.8 etc..)",
                "Kms_Driven": "Integer Vlaue lms (35000)",
                "Owner": "Integer Value  (0 or 1 or 3)",
                "Fuel_Type_Petrol": "String Value (Petrol / Diesel)",
                "Seller_Type_Individual": "String Value (Individual / Dealer)",
                "Transmission_Manual": "String Value (Manual / Automatic)"
            },
            
            'example':{
                "Year": 2016,
                "Present_Price": 8.5,
                "Kms_Driven": 35000,
                "Owner": 2 ,
                "Fuel_Type_Petrol": "Petrol",
                "Seller_Type_Individual": "Individual",
                "Transmission_Manual": "Manual"
            }
            
        }
        return Response(data)
    
    def post(self, request, format=None):
        
        Year = request.data['Year']
        Present_Price = request.data['Present_Price']
        Kms_Driven = request.data['Kms_Driven']
        Kms_Driven2=np.log(Kms_Driven)
        Owner = request.data['Owner']
        Fuel_Type_Petrol = request.data['Fuel_Type_Petrol']
        Seller_Type_Individual = request.data['Seller_Type_Individual']
        Transmission_Manual = request.data['Transmission_Manual']
        
        
        Year=2021-Year
        
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0 #CNG
            Fuel_Type_Diesel=0
            
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
            
        if(Transmission_Manual=='Manual'): #Automatic
            Transmission_Manual=1
        else:
            Transmission_Manual=0
            
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        
        output=round(prediction[0],2)
        if output<0:
            return Response({"message":"Sorry you cannot sell this car"})
        else:
            return Response({"predicted_price":"The car can be sold for {} lakhs approximately.".format(output)})
        
        