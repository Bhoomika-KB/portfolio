from django.shortcuts import render
# from myproject.shop.models import Contact

# Create your views here.
def portfolio(request):
    # if request.method=="POST":
    #     name = request.POST.get('name', '')
    #     email = request.POST.get('email', '')
    #     phone = request.POST.get('phone', '')
    #     desc = request.POST.get('desc', '')
    #     contact = Contact(name=name, email=email, phone=phone, desc=desc)
    #     contact.save()
    return render(request,'portfolio/index.html')