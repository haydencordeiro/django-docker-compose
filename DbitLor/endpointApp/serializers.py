
from rest_framework import serializers
from .models import *
from datetime import datetime
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        models = Status
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    # userR = UserSerializer(source='user_set', many=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(StudentProfileSerializer,
                    self).to_representation(instance)
        for i in instance.user._meta.fields:
            if i.name != "password":
                rep[str(i.name)] = getattr(instance.user, str(i.name))

        try:
            rep["last_login"] = instance.user.last_login.strftime(
                '%y-%m-%d %a %I:%M:%S')
        except:
            pass
        rep['dept'] = instance.dept.name
        return rep


class TeacherProfileSerializer(serializers.ModelSerializer):
    # userR = UserSerializer(source='user_set', many=True)

    class Meta:
        model = TeacherProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(TeacherProfileSerializer,
                    self).to_representation(instance)
        for i in instance.user._meta.fields:
            if i.name != "password":
                rep[str(i.name)] = getattr(instance.user, str(i.name))

        try:
            rep["last_login"] = instance.user.last_login.strftime(
                '%y-%m-%d %a %I:%M:%S')
        except:
            pass
        rep['dept'] = instance.dept.name
        return rep


class ApplicationSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer()
    teacher = TeacherProfileSerializer()
    # status = StatusSerializer()

    class Meta:
        model = Application
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(ApplicationSerializer,
                    self).to_representation(instance)
        rep['status'] = instance.status.status
        rep['time'] = instance.time.strftime("%I:%M %p")
        return rep


class DepartmentSerializer(serializers.ModelSerializer):
    # userR = UserSerializer(source='user_set', many=True)

    class Meta:
        model = Department
        fields = '__all__'

    # def to_representation(self, instance):
    #     rep = super(TeacherProfileSerializer,
    #                 self).to_representation(instance)
    #     for i in instance.user._meta.fields:
    #         if i.name != "password":
    #             rep[str(i.name)] = getattr(instance.user, str(i.name))

    #     try:
    #         rep["last_login"] = instance.user.last_login.strftime(
    #             '%y-%m-%d %a %I:%M:%S')
    #     except:
    #         pass
    #     return rep
