from django.contrib import admin
from .models import *

from django.apps import apps


# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except:
#         pass


class NotificationTokenListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in NotificationToken._meta.fields if True]


admin.site.register(NotificationToken, NotificationTokenListAdmin)


class DepartmentListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Department._meta.fields if True]


admin.site.register(Department, DepartmentListAdmin)


class StudentProfileListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in StudentProfile._meta.fields if True]


admin.site.register(StudentProfile, StudentProfileListAdmin)


class TeacherProfileListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in TeacherProfile._meta.fields if True]


admin.site.register(TeacherProfile, TeacherProfileListAdmin)


class ApplicationListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Application._meta.fields if True]


admin.site.register(Application, ApplicationListAdmin)


class StatusListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Status._meta.fields if True]


admin.site.register(Status, StatusListAdmin)
