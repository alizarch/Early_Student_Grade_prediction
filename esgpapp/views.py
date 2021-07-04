from enum import Flag
from django.shortcuts import render, redirect
from .validations import SignUpForm, loginform
import re
from django.contrib import messages
from django.contrib.auth.hashers import make_password , check_password
from .models import Users, CSV_Content
from django.contrib.auth import login, logout, authenticate
import csv, io
from io import StringIO
from .Helper import predict , checks



########### 0 ###########

def landingpage(request):
    if not request.user.is_authenticated:
        return render (request, 'others/landingpage.html')
    else:
        return redirect("dashboard")

########### 1 ###########

def signup(request):
    if not request.user.is_authenticated:
        return render (request, 'others/signup.html')
    else:
        return redirect("dashboard")

########### 2 ###########

def signuppost(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            su = SignUpForm(request.POST)
            if not su.is_valid():
                data = { 'forms' : su }
                return render (request, 'others/signup.html' ,data)

            phone = request.POST.get('pnumber')
            m = re.fullmatch("[9][2][3]\d{9}",phone)
            email = request.POST.get('email')
            email1 = Users.objects.filter(email = email).first()
            if m != None :
                if email1 == None:
                    fullname = request.POST.get('name')
                    dob=request.POST.get('dob')
                    fos=request.POST.get('fos')
                    password=request.POST.get('psw')
                    enc_password = make_password(password)
                    register = Users(
                            name = fullname, 
                            email = email, 
                            phone_number = phone, 
                            date_of_birth= dob , 
                            faculty_or_student = fos,
                            password= enc_password
                            )
                    register.save()
                    messages.success(request,'USER SUCCESSFULLY SAVED!!')
                    return redirect ('signup')
                else:
                    messages.error(request,'Email Already Exists!!')
                    return redirect ('signup')
            else:
                messages.error(request,'Please enter valid phone number i.e 923*********')
                return redirect ('signup') 
        else:
            messages.error(request,'GET request')
            return redirect ('signup')
    else:
        return redirect("dashboard")

########### 3 ###########

def user_login(request):
    if not request.user.is_authenticated:
        return render (request, 'others/login.html')
    else:
        return redirect("dashboard")

########### 4 ###########

def loginpost(request):
    if not request.user.is_authenticated:
        equest.POST.get('psw')
            user = Users.objects.filter(email= email).first()
            if user is not None:
                encrypted = user.password
                if check_password(upass, encrypted):
                    logif request.method == 'POST':
            lin = loginform(request.POST)
            if not lin.is_valid():
                data = { 'forms' : lin }
                return render (request, 'others/login.html' ,data)

            email = request.POST.get('email')
            upass = rin(request,user)
                    #messages.success(request,'Logged in Successfully')
                    return redirect("dashboard")
                else:
                    messages.error(request,'email and password is incorrect')
                    return redirect('login')
            else:
                messages.error(request, 'email not exists')
                return redirect('login')
        else:
            return redirect('login')
    else:
        return redirect("dashboard")

########### 5 ###########

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'others/dashboard.html',{'name': request.user})
    else:
        return redirect('landingpage')

########### 6 ###########

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('landingpage')
    else:
        return redirect('landingpage')

########### 7 ###########

def CalculatePrediction(request):
    if request.user.is_authenticated:
        if request.user.faculty_or_student == "Student":
            return render(request, "others/stu_cal_pre.html", {'name': request.user})
        else:
            return render(request, "others/fac_cal_pre.html", {'name': request.user})
    else:
        return redirect('landingpage')

########### 8 ###########

def upload_csv_file_faculty(request):
    try:
        if request.user.is_authenticated:
            if request.method == "GET":
                return redirect('cal_pre')

            if request.method == "POST":
                #Taking Uploaded File
                csv_files = request.FILES['student_file']
                
                #Validation Uploaded File
                if not csv_files.name.endswith('.csv'):
                    messages.error(request, 'Please choose csv file')
                    return redirect('cal_pre')

                #Reading & Inserting File Data To DB
                dataset = csv_files.read().decode('utf8') 
                io_string = io.StringIO(dataset)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar='|'):
                    created = CSV_Content.objects.update_or_create(
                        student_id=column[0],
                        student_name=column[1],
                        total_quizes=column[2],
                        given_quizes=column[3],
                        total_marks_of_quizes=column[4],
                        obtain_marks_in_quizes=column[5],
                        total_assignments=column[6],
                        given_assignments=column[7],
                        total_marks_of_assignments=column[8],
                        obtain_marks_in_assignments=column[9],
                        total_classes=column[10],
                        taken_classes=column[11],
                        last_month_grade=column[12],
                    )

                #Prediction
                users = CSV_Content.objects.all()
                pre = predict(users)

                #Return
                messages.success(request, 'Predicted')
                return render(request, 'others/fac_cal_pre.html', {'flag' : True, 'name': request.user})
        else:
                return redirect('Landingpage')
    except:
        messages.error(request, 'Excel file type must be of "CSV UTF-8" type.')
        return redirect('cal_pre')

########### 9 ###########

def upload_data_student(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return redirect('upload_student_data_result')

        if request.method == "POST":
            student_id = request.POST.get('s_id')
            student_name = request.POST.get('s_name')
            total_quizes = request.POST.get('total_q')
            given_quizes = request.POST.get('given_q')
            total_marks_of_quizes = request.POST.get('total_marks_of_q')
            obtain_marks_in_quizes = request.POST.get('obtain_marks_of_q')
            total_assignments = request.POST.get('total_a')
            given_assignments = request.POST.get('given_a')
            total_marks_of_assignments = request.POST.get('total_marks_of_a')
            obtain_marks_in_assignments = request.POST.get('obtain_marks_of_a')
            total_classes = request.POST.get('total_classes')
            taken_classes = request.POST.get('taken_classes')
            previous_grade = request.POST.get('previous_grades')

            #Checks
            msg = checks(
                total_quizes,
                given_quizes,
                total_marks_of_quizes,
                obtain_marks_in_quizes,
                total_assignments,
                given_assignments,
                total_marks_of_assignments,
                obtain_marks_in_assignments,
                total_classes,
                taken_classes,
            )
            if msg:
                messages.error(
                    request, msg
                )
                return redirect('cal_pre')

            CSV_Content.objects.update_or_create(
                student_id = student_id,
                student_name = student_name,
                total_quizes = total_quizes,
                given_quizes = given_quizes,
                total_marks_of_quizes = total_marks_of_quizes,
                obtain_marks_in_quizes = obtain_marks_in_quizes,
                total_assignments = total_assignments,
                given_assignments = given_assignments,
                total_marks_of_assignments = total_marks_of_assignments,
                obtain_marks_in_assignments = obtain_marks_in_assignments,
                total_classes = total_classes,
                taken_classes = taken_classes,
                last_month_grade = previous_grade,
            )

            #Prediction
            users = CSV_Content.objects.all()
            pre = predict(users)

            #Take predicted row
            predict_data = CSV_Content.objects.first()

            return render(
                request,
                "others/stu_cal_pre_result.html",
                {'name': request.user, 'predict_data': predict_data}
            )
    else:   
            return redirect('Landingpage')

########### 10 ###########

def upload_data_student_result(request):
    if request.user.is_authenticated:
        predict_data = CSV_Content.objects.first()
        return render(
            request,
            "others/stu_cal_pre_result.html",
            {'name': request.user, 'predict_data': predict_data}
        )
    else:
        return redirect('landingpage')
