from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from user.models import User
from .models import Key
from django.http import Http404
from .serializers import UserSerializer,KeySerializer
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
        serialized.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class ListKeys(generics.ListAPIView):

    def get_queryset(self):
        return Key.objects.filter(user=self.request.user)

    def list(self, request,  *args, **kwargs):
        queryset = self.get_queryset()
        serializer = KeySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PutKey(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KeySerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer.save(user=user)
        return Response(status=status.HTTP_200_OK)


class GetKey(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KeySerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.request.user.id)
        return serializer.save(user=user)


class UpdateKey(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Key.objects.all()
    serializer_class = KeySerializer
    lookup_field = 'slug'

    def get_object(self, slug):
        return get_object_or_404(Key, slug = slug)

    def update(self, request, *args, **kwargs):
        slug_val = self.kwargs['slug']
        key = self.get_object(slug_val)
        if key.user == self.request.user:
            serializer = KeySerializer(key, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)