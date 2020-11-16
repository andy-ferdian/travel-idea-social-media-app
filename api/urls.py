from django.urls import path, include
from .views import *
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# API Router #
router = routers.DefaultRouter()

router.register(prefix='fullrestaurants', viewset=FullRestaurantView, basename='fullrestaurants')
router.register(prefix='restaurants', viewset=RestaurantView, basename='restaurants')
router.register(prefix='location', viewset=LocationView, basename='location')
router.register(prefix='restaurantimages', viewset=RestaurantImagesView, basename='restaurantimages')
router.register(prefix='restaurantmenus', viewset=RestaurantMenusView, basename='restaurantmenus')

urlpatterns = [
    path('', include(router.urls), name='api'),
]
