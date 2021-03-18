from django.shortcuts import render,redirect
from .models import Student, Teacher, ClassRoom
from django.core.mail import send_mail
from myproject import settings


# Create your views here.
def homepage(request):
    all_classes = ClassRoom.objects.all()

    user_obj=None

    if request.session.has_key('role') and request.session.has_key('id'):
        if request.session['role']=='teacher':
            user_obj=Teacher.objects.get(id=request.session['id'])

        if request.session['role']=='student':
            user_obj=Student.objects.get(id=request.session['id'])

    if request.method=='POST':
        class_name=request.POST.get('class')

        try:
            c=ClassRoom(class_name=class_name)
            c.save()

        except :
            c=ClassRoom.objects.get(class_name=class_name)
            message="The Class Room is already Present"
            return render(request, 'studentapp/homepage.html',{'all_classes':all_classes,'user_obj':user_obj,'message':message})


    return render(request, 'studentapp/homepage.html',{'all_classes':all_classes,'user_obj':user_obj})

def single_class(request,id):
    single_class=  ClassRoom.objects.filter(id=id).first()
    teachers=  ClassRoom.objects.filter(id=id).first().teacher.all()

    user_obj=None
    if request.session.has_key('role') and request.session.has_key('id'):
        if request.session['role']=='teacher':
            user_obj=Teacher.objects.get(id=request.session['id'])


        if request.session['role']=='student':
            user_obj=Student.objects.get(id=request.session['id'])

    return render(request, 'studentapp/single_class.html',{'single_class':single_class, 'teachers':teachers ,'user_obj':user_obj})

def login(request):
    error = None
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        role=request.POST.get('option')

        if email=='' or password=='':
            error = "The email or password cannot be empty"
            return render(request, 'studentapp/login.html',{'error':error})

        if role =='student':
            try:
                user_obj= Student.objects.get(email=email,password=password)
                request.session['role'] = user_obj.role
                request.session['id'] = user_obj.id
                return redirect('homepage')
            except :
                error = "Wrong Credentials or Role"
                return render(request, 'studentapp/login.html',{'error':error})
        else:
            try:
                user_obj= Teacher.objects.get(email=email,password=password)
                request.session['role'] = user_obj.role
                request.session['id'] = user_obj.id
                return redirect('homepage')
            except :
                error = "Wrong Credentials or Role"
                return render(request, 'login.html',{'error':error})

    return render(request, 'studentapp/login.html',{'error':error})







def register(request,class_name):
    user_obj=None
    if request.session.has_key('role') and request.session.has_key('id'):
        if request.session['role']=='student':
            user_obj=Student.objects.get(id=request.session['id'])



    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        user_obj=None
        if request.session.has_key('role') and request.session.has_key('id'):
            if request.session['role']=='student':
                user_obj=Student.objects.get(id=request.session['id'])

        if email=='' or password1=='' or name=='' or password2=='':
            error = "The fields cannot be empty. Please fill all the fields."
            return render(request, 'studentapp/register.html',{'user_obj':user_obj,'error':error,'class_name':class_name})

        if password1!=password2:
            error = "Passwords Donot Match."
            return render(request, 'studentapp/register.html',{'user_obj':user_obj,'error':error,'class_name':class_name})



        if user_obj==None:
            try:
                student_obj = Student.objects.get(email=email)
                try:
                    c_obj=student_obj.classroom.get(class_name=class_name)
                    error = "You have already registered to this class room"
                    return render(request, 'studentapp/register.html',{'user_obj':student_obj,'error':error,'class_name':class_name})
                except:
                    c_obj=ClassRoom.objects.get(class_name=class_name)
                    student_obj.classroom.add(c_obj)
                    student_obj.save()
                    message='old user class Registration successful'
                    student_name=student_obj.student_name
                    send_mail(settings.EMAIL_SUBJECT.format(student_name,class_name), settings.EMAIL_BODY.format(class_name), settings.EMAIL_HOST_USER, ['rajkamalraju41@gmail.com'], fail_silently = False)
                    return render(request, 'studentapp/register.html',{'user_obj':student_obj,'message':message,'class_name':class_name})
            except:
                student_obj=Student(student_name=name, email=email, password=password1)
                student_obj.save()
                c_obj=ClassRoom.objects.get(class_name=class_name)
                student_obj.classroom.add(c_obj)
                student_obj.save()
                message="New user with classroom registration completed"
                student_name=student_obj.student_name
                send_mail(settings.EMAIL_SUBJECT.format(student_name,class_name), settings.EMAIL_BODY.format(class_name), settings.EMAIL_HOST_USER, ['rajkamalraju41@gmail.com'], fail_silently = False)
                return render(request, 'studentapp/register.html',{'message':message,'class_name':class_name})

        else:
            student_obj=user_obj
            try:
                c=student_obj.classroom.get(class_name=class_name)
            except :
                c=None

            if c!=None:
                error = "You have already registered to this class room when logged in"
                return render(request, 'studentapp/register.html',{'user_obj':student_obj,'error':error,'class_name':class_name})
            else:
                c_obj=ClassRoom.objects.get(class_name=class_name)
                student_obj.classroom.add(c_obj)
                student_obj.save()
                message='old user class Registration successful user already loggedin'
                # # email(user_obj.student_name,c.class_name,subjects,user_obj.email)
                # email("RAJ","CLASSROOM1","datascie pythion","rajkamalraju41@gmail.com")
                student_name=student_obj.student_name
                send_mail(settings.EMAIL_SUBJECT.format(student_name,class_name), settings.EMAIL_BODY.format(class_name), settings.EMAIL_HOST_USER, ['rajkamalraju41@gmail.com'], fail_silently = False)

                return render(request, 'studentapp/register.html',{'user_obj':student_obj,'message':message,'class_name':class_name})



    return render(request, 'studentapp/register.html',{'user_obj':user_obj,'class_name':class_name})

def logout(request):
    try:
      del request.session['role']
      del request.session['id']

    except:
      print('Not able to delete session')
    return redirect('login')

def profile(request):
    if request.session.has_key('role') and request.session.has_key('id'):
        if request.session['role']=='teacher':
            user_obj=Teacher.objects.get(id=request.session['id'])
        if request.session['role']=='student':
            user_obj=Student.objects.get(id=request.session['id'])


    return render(request, 'studentapp/profile.html',{'user_obj':user_obj})


def about_page(request):
    return render(request,'studentapp/about_page.html')