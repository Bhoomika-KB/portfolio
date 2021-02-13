from django.shortcuts import render
import requests
import json

# Create your views here.
def covid(request):
    context = {}
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
    headers = {
        'x-rapidapi-key': "2c1280413bmsh6b3386dc04fcae5p1fa8dejsnbb6731a7f503",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers)
    
    #Total list
    main_dict_list = response.json()["data"]["covid19Stats"]
    context["main_dict_list"]=main_dict_list
    
    #Total Confirmed
    total_confirmed = 0
    for row in main_dict_list:
        total_confirmed = total_confirmed + row["confirmed"]  
    context["total_confirmed"]=total_confirmed  
    
    #Total deaths
    total_deaths = 0
    for row in main_dict_list:
        total_deaths = total_deaths + row["deaths"]  
    context["total_deaths"]=total_deaths  
    
    #Total recovered
    total_recovered = 0
    for row in main_dict_list:
        if row["recovered"]==None:
            continue
        else: 
            total_recovered = total_recovered+row["recovered"]
    context["total_recovered"]=total_recovered 
    
    
    
    #Unique Country List
    unique_country_list = list(set([dic["country"] for dic in main_dict_list]))
    unique_country_list.sort()
    context["unique_country_list"] = unique_country_list
    
    
    context["country_stats"]=["Select The Country",0, 0, 0]
    
    if request.method=="POST":
        country_name=request.POST["submit"]
        
        total_country_deaths=0
        total_country_recovered=0
        total_country_confirmed=0
        
        for dic in main_dict_list:
            if dic["country"] == country_name:             
                total_country_deaths =  total_country_deaths + dic["deaths"]  
                if dic["recovered"]==None:
                    continue
                else:
                    total_country_recovered =  total_country_recovered + dic["recovered"]           
                total_country_confirmed =  total_country_confirmed + dic["confirmed"]
        context["country_stats"]=[country_name,total_country_confirmed, total_country_deaths, total_country_recovered]
        return render(request, 'covid.html', context=context)
                
           
    
    return render(request, 'covid.html', context=context)