import pdb
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator, ValidationError
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from pdb import set_trace
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'name',)


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name', 'longitude', 'latitude',)


class RestaurantImageSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), many=False, required=False)

    class Meta:
        model = RestaurantImageFile
        fields = ('id', 'restaurant', 'img_file',)


class RestaurantMenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), many=False, required=False)

    class Meta:
        model = RestaurantMenuFile
        fields = ('id', 'restaurant', 'menu_file',)


class RestaurantSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)
    category = CategorySerializer(many=False)
    restaurant_images = RestaurantImageSerializer(source='restaurantimagefile_set', many=True, required=False)
    restaurant_menus = RestaurantMenuSerializer(source='restaurantmenufile_set', many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'category', 'location', 'restaurant_images',  'restaurant_menus',)


    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        category_data = validated_data.pop('category', None)
        images_data = validated_data.pop('restaurantimagefile_set', None)
        menus_data = validated_data.pop('restaurantmenufile_set', None)

        
        if location_data:
            location = Location.objects.create(**location_data)
        else:
            location = None

        restaurant = Restaurant.objects.create(location=location, **validated_data)

        if category_data:
            category_id = category_data.get('id', None)
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                    restaurant.category = category
                    restaurant.save()
                except Category.DoesNotExist:
                    raise ValidationError('Category %s does not exist.' % category_id)
            else:
                category = Category.objects.create(name=category_data['name'])
                restaurant.category = category
                restaurant.save()

        if images_data:
            for image in images_data:
                RestaurantImageFile.objects.create(restaurant=restaurant, **image)

        if menus_data:
            for menu in menus_data:
                RestaurantMenuFile.objects.create(restaurant=restaurant, **menu)

        return restaurant



class FullRestaurantSerializer(serializers.ModelSerializer):
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
