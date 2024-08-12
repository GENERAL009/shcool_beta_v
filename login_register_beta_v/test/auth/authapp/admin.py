from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "role",)
    list_display_links = ("user",
                          )


class ClasAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "subject",)


# Register your models here.
admin.site.register(Subject, )
admin.site.register(Class, ClasAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Student, )
admin.site.register(Teacher, )
admin.site.register(Grade)
