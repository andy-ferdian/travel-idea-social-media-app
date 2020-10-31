from django.contrib import admin
from .models import *


# Register your models here.
model = [Restaurant, Attraction, Comment, Review, Location, Category, HowToGetThere, RestaurantImageFile, AttractionImageFile, CommentImageFile, ReviewImageFile, RestaurantMenuFile]
admin.site.register(model)
