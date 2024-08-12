from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='login'),
    path('teacher_register/', teacher_register, name='teacher_register'),
    path('student_register/', student_register, name='student_register'),
    path('teacher/dashboard/<int:teacher_id>/', teacher_dashboard, name='teacher_dashboard'),
    path('subject/<int:subject_id>/', subject_dashboard, name='subject_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('logout/', user_logout, name='logout'),
    path('class/<int:class_id>/<int:subject_id>/', class_detail, name='class_detail'),
    path('student/class/<int:class_id>/<int:subject_id>/', student_class_detail, name='student_class_detail'),

]
