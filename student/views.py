from django.shortcuts import render, redirect
from django.contrib import messages
from STUDENT.models import *
from FACULTY.models import *
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from datetime import date
from collections import defaultdict
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def home(request):
    return render(request,'home.html')

def stu_regi(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        c_pass = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        batch = request.POST.get('batch')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        print('gwduhyfbgrhujyfgbhhjvbhj')
        if not name or not email or not phone or not  address or not address or not password or not c_pass or not image or not batch or not year or not semester:
            messages.error(request,'plaes fill all the fileds')
            return redirect('stu_regi')
        print('edgwuyfbvhjvhbdjvhbhjvbvh')
        if password != c_pass:
            messages.error(request, 'Password does not match')
            return redirect('stu_regi')

        # 🔹 Generate College ID
        college_id = generate_college_id(batch)

        # 🔹 Save Student
        student = Student.objects.create(
            college_id=college_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            password=password,
            batch=batch,
            year=year,
            semester=semester,
            images = image
        )

        # 🔹 Send Email
        send_mail(
            subject="College ID Registration Successful",
            message=f"""
Hello {student.name},

Welcome to our college!

Your registration is successful.
Here are your details:

College ID : {student.college_id}
Batch      : {student.batch}
Year       : {student.get_year_display()}
Semester   : {student.get_semester_display()}

Please keep this ID safe. You will use it for:
- Login
- Attendance
- Results
- Official Records

Regards,
College Administration
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=False
        )

        messages.success(request, 'Student registered successfully. College ID sent to email.')
        return redirect('stu_login')

    return render(request, 'stu_regi.html')

def generate_college_id(batch):
    batch_year = batch.split('-')[0]  
    last_student = (
        Student.objects
        .filter(college_id__contains=batch_year)
        .order_by('-id')
        .first()
    )

    if last_student:
        last_number = int(last_student.college_id.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"TKC-{batch_year}-{str(new_number).zfill(4)}"

def stu_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        college_id = request.POST.get('college_id')
        password = request.POST.get('password')

        if not email or not password or not college_id:
            messages.error(request,'please fill all the fileds')
            return redirect('stu_login')
        
        try:
            student = Student.objects.get(email=email, password=password)

            request.session['student_id'] = student.id
            request.session['stu_name'] = student.name
            request.session['stu_mail'] = student.email

            messages.success(request,'student login successfully')
            return redirect('stu_dash')
        
        except Student.DoesNotExist:
            messages.error(request,'invalid credentials')
            return redirect('stu_login')

    return render(request,'stu_login.html')

def stu_dash(request):
    return render(request,'stu_dash.html')

def fac_regi(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        c_pass = request.POST.get('c_pass')
        image = request.FILES.get('image')

        if not name or not email or not phone or not address or not password or not c_pass or not image:
            messages.error(request,'please fill all the fileds')
            return redirect('fac_regi')
        
        if password != c_pass:
            messages.error(request,'password doesnot match')
            return redirect('fac_regi')
        
        if Teacher.objects.filter(email=email).exists():
            messages.error(request,'email already exixts please use another email')
            return redirect('fac_regi')
        
        new_fac = Teacher(
            name = name,
            email = email,
            address = address,
            password = password,
            phone = phone,
            image = image
        )
        new_fac.save()
        messages.success(request,'Faculty registered successfully')
        return redirect('fac_login')
    return render(request,'fac_regi.html')

def fac_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request,'please fill all the fileds')
            return redirect('fac_login')
        
        try:
            teacher = Teacher.objects.get(email=email, password=password)

            request.session['fac_id'] = teacher.id
            request.session['fac_mail'] = teacher.email
            request.session['fac_name'] = teacher.name

            messages.success(request,'teacher scuuesfully login')
            return redirect('fac_dash')
        
        except Teacher.DoesNotExist:
            messages.error(request,'invalid credentials')
            return redirect('fac_login')
        
    return render(request,'fac_login.html')

def fac_dash(request):
    name = request.session.get('fac_name')
    context = {
        'name' :name
    }
    return render(request,'fac_dash.html',context)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            messages.success(request,'admin login successfully')
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials.")
            return redirect('admin_login')
    return render(request,'admin_login.html')

def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    return render(request,'admin_dashboard.html',{'admin_user': request.user})

def admin_logout(request):
    auth_logout(request)
    messages.success(request,'Admin logout successfully')
    return redirect('home')

def logout(request):
    request.session.flush()
    return redirect('home')

def view_faculty(request):
    faculties = Teacher.objects.all()
    return render(request, 'view_faculty.html', {
        'faculties': faculties
    })

def view_students(request):
    students = Student.objects.all()
    return render(request, 'view_students.html', {
        'students': students
    })


def view_students_fac(request):
    students = Student.objects.all()
    context = {
        'students' : students
    }
    return render(request,'view_students_fac.html',context)

def post_attendance(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    print(subjects)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        subject_id = request.POST.get('subject')
        period = request.POST.get('period')
        status = request.POST.get('status')

        if not student_id:
            messages.error(request, 'Please select a student')
            return redirect('post_attendance')

        student = Student.objects.get(id=student_id)

        # ❌ SUBJECT already used today
        if Attendance.objects.filter(
            student=student,
            date=date,
            subject_id=subject_id
        ).exists():
            messages.error(
                request,
                'This subject is already assigned for this day'
            )
            return redirect('post_attendance')

        # ❌ PERIOD already used today
        if Attendance.objects.filter(
            student=student,
            date=date,
            period=period
        ).exists():
            messages.error(
                request,
                'This period is already assigned for this day'
            )
            return redirect('post_attendance')

        Attendance.objects.create(
            student=student,
            subject_id=subject_id,
            date=date,
            period=period,
        )