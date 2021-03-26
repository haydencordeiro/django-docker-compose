
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init, pre_init
import requests


def sendNotification(usertoken, title, body):
    userdata = {
        "to": str(usertoken),
        "body": str(body),
        "title": str(title),



    }
    headers = {
        "Content-Type": "application/json"

    }
    r = requests.post(
        'https://exp.host/--/api/v2/push/send/',  json=userdata, headers=headers)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    dept = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    yearofpassout = models.CharField(max_length=4, null=True)
    studentID = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    dept = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s's profile" % self.user


class Status(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return str(self.status)


class Application(models.Model):

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(
        TeacherProfile, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return (self.status.status)

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')

        if instance.status.status == "pending":
            teacher = NotificationToken.objects.filter(
                user=instance.teacher.user).first()
            sendNotification(teacher.token, "LOR Request",
                             "{} has request for an LOR".format(instance.student))

    @ staticmethod
    def remember_status(sender, **kwargs):
        instance = kwargs.get('instance')


post_save.connect(Application.post_save, sender=Application)
post_init.connect(Application.remember_status, sender=Application)


class NotificationToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.token
