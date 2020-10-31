from django.urls import path, include
from .views import *
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# API Router #
router = routers.DefaultRouter()

router.register(prefix='restaurant', viewset=RestaurantView, basename='restaurant')

urlpatterns = [
    path('', include(router.urls), name='api'),
]
