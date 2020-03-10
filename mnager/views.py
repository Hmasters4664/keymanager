from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from user.models import User
from .models import KeyRecord
from django.http import Http404
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .keepassfunctions import createfile
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters
# Create your views here.


@csrf_exempt
@api_view(['POST'])
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.save()
        key = KeyRecord(user=user)
        key.save()
        createfile(key.file)
        content = {'200': 'Ok'}
        return Response(serialized.data,status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)