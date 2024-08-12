# myapp/views.py
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from .forms import LoginForm, TeacherRegistrationForm, StudentRegistrationForm
from .models import *
from datetime import date, timedelta, datetime
from django.http import HttpResponseRedirect
from django.http import JsonResponse


@csrf_protect
@ensure_csrf_cookie
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                auth_login(request, user)
                if hasattr(user, 'profile'):
                    if user.profile.role == 'teacher':
                        teacher = Teacher.objects.get(user=user)
                        if teacher.subjects.exists():
                            subject = teacher.subjects.first()
                            return redirect('subject_dashboard', subject_id=subject.id)
                        else:
                            messages.error(request, 'No subjects assigned to this teacher!')
                            return redirect('login')
                    elif user.profile.role == 'student':
                        return redirect('student_dashboard')
                    else:
                        messages.error(request, 'User role is not defined!')
                        return redirect('login')
                else:
                    messages.error(request, 'User profile not found!')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'title': 'Sign in',
        'form': form
    }

    return render(request, 'login.html', context)


@csrf_protect
@ensure_csrf_cookie
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.update_or_create(user=user, defaults={'role': 'teacher'})
            teacher, created = Teacher.objects.get_or_create(user=user)
            teacher.subjects.set(form.cleaned_data.get('subjects'))
            teacher.save()
            messages.success(request, 'Teacher signed up successfully!')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('teacher_register')
    else:
        form = TeacherRegistrationForm()
    subjects = Subject.objects.all()
    context = {
        'title': 'Teacher Sign Up',
        'form': form,
        'subjects': subjects
    }

    return render(request, 'teacher_register.html', context)


@csrf_protect
@ensure_csrf_cookie
def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.update_or_create(user=user, defaults={'role': 'student'})
            messages.success(request, 'Student signed up successfully!')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('student_register')
    else:
        form = StudentRegistrationForm()

    context = {
        'title': 'Student Sign Up',
        'form': form
    }

    return render(request, 'student_register.html', context)


@login_required
def teacher_dashboard(request, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    subjects = teacher.subjects.all()
    return render(request, 'teacher_dashboard.html', {'title': 'Teacher Dashboard', 'subjects': subjects})


@login_required
def subject_dashboard(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    classes = Class.objects.filter(subject=subject)
    return render(request, 'subject_dashboard.html', {'title': subject.name, 'subject': subject, 'classes': classes})


def user_logout(request):
    auth_logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


@login_required
def student_dashboard(request):
    if request.user.profile.role == 'student':
        student = get_object_or_404(Student, user=request.user)
        classes = Class.objects.filter(student=student)
        subjects_with_classes = [
            {'subject': class_obj.subject, 'class_id': class_obj.id}
            for class_obj in classes
        ]
        return render(request, 'student_dashboard.html',
                      {'title': 'Your Subjects', 'subjects_with_classes': subjects_with_classes})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('login')


@login_required
def class_detail(request, class_id, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    class_obj = get_object_or_404(Class, pk=class_id)
    students = class_obj.student.all()

    if request.method == 'POST':
        # Обработка POST-запроса
        for student in students:
            for date_str in request.POST.getlist('date'):
                grade = request.POST.get(f'grade_{student.id}_{date_str}')
                if grade:
                    Grade.objects.update_or_create(
                        student=student,
                        subject=subject,
                        date=date_str,
                        defaults={'grade': grade},
                    )

    # Установка начальных и конечных дат
    start_date = request.GET.get('start_date', (date.today() - timedelta(days=14)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', date.today().strftime('%Y-%m-%d'))

    start_date_obj = date.fromisoformat(start_date)
    end_date_obj = date.fromisoformat(end_date)

    dates = [start_date_obj + timedelta(days=x) for x in range((end_date_obj - start_date_obj).days + 1)]

    student_grades = []
    for student in students:
        student_grade_data = {'student': student, 'grades': []}
        for day in dates:
            date_str = day.strftime('%Y%m%d')
            grade = Grade.objects.filter(student=student, subject=subject, date=date_str).first()
            student_grade_data['grades'].append(
                {'date': date_str, 'grade': grade.grade if grade else None}
            )
        student_grades.append(student_grade_data)

    context = {
        'subject': subject,
        'class': class_obj,
        'students': students,
        'dates': dates,
        'student_grades': student_grades,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'class_detail.html', context)


@login_required
def student_class_detail(request, class_id, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    class_obj = get_object_or_404(Class, pk=class_id)
    student = get_object_or_404(Student, user=request.user)

    # Установка начальных и конечных дат
    start_date = request.GET.get('start_date', (date.today() - timedelta(days=14)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', date.today().strftime('%Y-%m-%d'))

    start_date_obj = date.fromisoformat(start_date)
    end_date_obj = date.fromisoformat(end_date)

    dates = [start_date_obj + timedelta(days=x) for x in range((end_date_obj - start_date_obj).days + 1)]

    student_grades = []
    student_grade_data = {'student': student, 'grades': []}
    for day in dates:
        date_str = day.strftime('%Y%m%d')
        grade = Grade.objects.filter(student=student, subject=subject, date=date_str).first()
        student_grade_data['grades'].append(
            {'date': date_str, 'grade': grade.grade if grade else None}
        )
    student_grades.append(student_grade_data)

    context = {
        'subject': subject,
        'class': class_obj,
        'student': student,
        'dates': dates,
        'student_grades': student_grades,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'student_class_detail.html', context)
