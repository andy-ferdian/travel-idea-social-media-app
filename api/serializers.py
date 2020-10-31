import pdb
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from pdb import set_trace
from .models import *



class RestaurantSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    longitude = serializers.CharField(source='location.longitude')
    latitude = serializers.CharField(source='location.latitude')
    restaurant_images = serializers.SerializerMethodField()
    restaurant_menus = serializers.SerializerMethodField()
    restaurant_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'category', 'longitude', 'latitude', 'restaurant_images', 'restaurant_menus', 'restaurant_reviews',)

    def get_restaurant_images(self, obj):
        instances = []
        request = self.context.get('request')

        if obj.restaurantimagefile_set:
            for restaurant_image in obj.restaurantimagefile_set.all():
                
                image_url = request.build_absolute_uri(restaurant_image.file.url)
                instances.append(image_url)
        
        return instances

    
    def get_restaurant_menus(self, obj):
        instances = []
        request = self.context.get('request')

        if obj.restaurantmenufile_set:
            for restaurant_menu in obj.restaurantmenufile_set.all():
                
                menu_url = request.build_absolute_uri(restaurant_menu.file.url)
                instances.append(menu_url)
        
        return instances


    def get_restaurant_reviews(self, obj):
        instances = []
        request = self.context.get('request')

        if obj.review_set:
            for restaurant_review in obj.review_set.all():
                review = {'user' : restaurant_review.user.username, 'rating' : restaurant_review.rating, 'content': restaurant_review.content}
                review_images = ReviewImageFile.objects.filter(review=restaurant_review.id)
                if review_images:
                    rev_images = []
                    for review_image in review_images:
                        review_image_url = request.build_absolute_uri(review_image.file.url)
                        rev_images.append(review_image_url)
                    review['review_images'] = rev_images
                instances.append(review)

        return instances
