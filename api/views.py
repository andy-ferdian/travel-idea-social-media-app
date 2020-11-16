from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *
from pdb import set_trace


# Create your views here.

class FullRestaurantView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = FullRestaurantSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class RestaurantView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class LocationView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class RestaurantImagesView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RestaurantImageFile.objects.all()
    serializer_class = RestaurantImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class RestaurantMenusView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RestaurantMenuFile.objects.all()
    serializer_class = RestaurantMenuSerializer

    def get_serializer_context(self):
        return {'request': self.request}