from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *
from pdb import set_trace


# Create your views here.

class RestaurantView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_context(self):
        return {'request': self.request}

