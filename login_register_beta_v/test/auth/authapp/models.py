# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

ROLE_CHOICES = [
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('admin', 'Admin'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subjects = models.ManyToManyField(Subject)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hours_taught = models.IntegerField(default=0)
    salary_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('teacher_dashboard', kwargs={'teacher_id': self.pk})


class Student(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


class Grade(models.Model):
    GRADE_CHOICES = [
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('-', 'Не был на уроке'),
        ('L', 'Опоздал'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    date = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} - {self.grade}"
