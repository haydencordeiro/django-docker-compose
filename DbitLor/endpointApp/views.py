from typing import Text
from django.shortcuts import render
from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
import time
from rest_framework.parsers import JSONParser
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect, HttpResponsePermanentRedirect)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth
import requests
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, date
from django.core.mail import send_mail
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
from django.views.decorators.cache import cache_control
from django.db.models import Sum
import collections
import json
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import requests

# from .render import Render
# add user to group
# from django.contrib.auth.models import Group
# my_group = Group.objects.get(name='my_group_name')
# my_group.user_set.add(your_user)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        teacher = TeacherProfileSerializer(
            TeacherProfile.objects.filter(user=user).first()).data
        student = StudentProfileSerializer(
            StudentProfile.objects.filter(user=user).first()).data

        custom_response = {
            'token': token.key,
        }
        if teacher['user'] == None:
            custom_response['whoami'] = "student"
            custom_response['user'] = student
        else:
            custom_response['whoami'] = "teacher"
            custom_response['user'] = teacher

        return Response(custom_response)

# check if user exist in group


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        if request.user.groups.filter(name="student").exists():  # is student
            try:
                user = StudentProfile.objects.get(user=request.user)
            except:
                return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = StudentProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:  # is teacher
            try:
                user = TeacherProfile.objects.get(user=request.user)
            except:
                return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = TeacherProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
@ permission_classes([IsAuthenticated])
def ListAllDepartments(request):
    if request.user.groups.filter(name="student").exists():
        dept = Department.objects.all()

        return Response(DepartmentSerializer(dept, many=True).data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


# Students

@api_view(('POST',))
@ permission_classes([IsAuthenticated])
def ApplyForLor(request):
    if request.user.groups.filter(name="student").exists():

        application = Application(
            student=StudentProfile.objects.filter(
                user=request.user).first(),
            teacher=TeacherProfile.objects.filter(
                user=User.objects.filter(id=request.data['teacherID']).first()).first(),
            status=Status.objects.get(status="pending"),
            content=request.data['content']

        )
        application.save()
        return Response(ApplicationSerializer(application).data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@ permission_classes([IsAuthenticated])
def ListAllTeachers(request):
    if request.user.groups.filter(name="student").exists():
        teachers = TeacherProfile.objects.all()

        return Response(TeacherProfileSerializer(teachers, many=True).data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@ permission_classes([IsAuthenticated])
def LoggedInUsersApplications(request):
    if request.user.groups.filter(name="student").exists():
        application = Application.objects.filter(student=StudentProfile.objects.filter(
            user=request.user).first()).order_by(*['-date', '-time'])

        return Response(ApplicationSerializer(application, many=True).data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


# Teachers

@api_view(('GET',))
@ permission_classes([IsAuthenticated])
def LoggedInTeachersApplications(request):
    if request.user.groups.filter(name="teacher").exists():
        application = Application.objects.filter(
            teacher=TeacherProfile.objects.filter(user=request.user).first()).order_by(*['-date', '-time'])
        return Response(ApplicationSerializer(application, many=True).data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
@ permission_classes([IsAuthenticated])
def LoggedInTeacherEditApplications(request):
    if request.user.groups.filter(name="teacher").exists():
        application = Application.objects.get(id=int(request.data['appID']))
        application.status = Status.objects.get(
            status=request.data['status'])
        application.content = request.data["content"]
        application.save()

        return Response(ApplicationSerializer(application).data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@ permission_classes([IsAuthenticated])
def DashboardStatsTeacher(request):
    if request.user.groups.filter(name="teacher").exists():
        application = Application.objects.filter(teacher=TeacherProfile.objects.filter(
            user=request.user).first())
        data = {

        }
        data['pendingReq'] = application.filter(
            status=Status.objects.get(status="pending")).count()
        data['approvedReq'] = application.filter(
            status=Status.objects.get(status="approved")).count()
        data['rejectedReq'] = application.filter(
            status=Status.objects.get(status="rejected")).count()
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


# Teachers


@api_view(('POST',))
@permission_classes([IsAuthenticated])
def generatePDF(request):
    if request.user.groups.filter(name="student").exists():
        application = Application.objects.filter(
            id=request.data['appID']).first()

        URL = "https://script.google.com/macros/s/AKfycbzm8_19fqeC4sWJEdHSFteRfhGsGFYqff6TDflPPNTRn0iKpff6LlVe/exec"

        f = {}
        f['invoice_id'] = str(request.user.first_name)+" " + \
            str(request.user.first_name)+" "+str(application.id)
        if(application.content != None):
            f['textC'] = application.content
        else:
            f['textC'] = ""

        # print(f)
        r = requests.get(url=URL, params=f)
        data = r.text

        return Response({'downloadLink': data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You Dont Have Permission To Access This'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST', 'GET'))
@permission_classes([IsAuthenticated])
def NotificationTokenView(request):

    temp = NotificationToken.objects.filter(user=request.user).first()
    if temp is None:

        temp = NotificationToken(
            user=request.user,
            token=request.data["token"]
        )
    else:
        temp.token = request.data["token"]
    temp.save()

    return Response({}, status=status.HTTP_200_OK)
