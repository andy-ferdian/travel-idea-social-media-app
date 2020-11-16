from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the category.')

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '%s' % (self.name)


class Location(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the location.')
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Locations'

    def __str__(self):
        return '%s - long: %s - lat: %s' % (self.name, self.longitude, self.latitude)


class Restaurant(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the restaurant.')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurant_category')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurant_location')

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        if self.category:
            return '%s - %s' % (self.name, self.category.name)
        else:
            return '%s - %s' % (self.name, "No category!")


class Attraction(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the attraction.')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='attraction_category')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='attraction_location')
    enterance_fee = models.TextField(null=True, help_text='Attraction enterance fee.')

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Attractions'

    def __str__(self):
        if self.category:
            return '%s - %s' % (self.name, self.category.name)
        else:
            return '%s - %s' % (self.name, "No category!")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True, blank=True, help_text="User rating (1-5).")
    content = models.TextField(blank=True, null=True)
    comment_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.content:
            return '%s - %s - %s' % (self.user.username, self.attraction.name, self.content)
        else:
            return '%s - %s - %s' % (self.user.username, self.attraction.name, "No content!")

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True, blank=True, help_text="User rating (1-5).")
    content = models.TextField(blank=True, null=True)
    review_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.content:
            return '%s - %s - %s' % (self.user.username, self.restaurant.name, self.content)
        else:
            return '%s - %s - %s' % (self.user.username, self.restaurant.name, "No content!")


class HowToGetThere(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_howtoget_there')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='attraction_howtoget_there')
    content = models.TextField(blank=True, null=True)
    post_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.content:
            return '%s - %s - %s' % (self.user.username, self.attraction.name, self.content)
        else:
            return '%s - %s - %s' % (self.user.username, self.attraction.name, "No content!")


class RestaurantImageFile(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_images', on_delete=models.CASCADE)
    file = models.FileField(upload_to='restaurant_images/', help_text='Restaurant image.', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.file:
            return '%s - %s' % (self.restaurant.name, self.file)
        else:
            return '%s - %s' % (self.restaurant.name, 'No Image!')


class RestaurantMenuFile(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_menus', on_delete=models.CASCADE)
    file = models.FileField(upload_to='restaurant_menu/', help_text='Restaurant Menu.', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.file:
            return '%s - %s' % (self.restaurant.name, self.file)
        else:
            return '%s - %s' % (self.restaurant.name, 'No Menu!')


class AttractionImageFile(models.Model):
    restaurant = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='attraction_image')
    file = models.FileField(upload_to='attraction_images/', help_text='Attraction image.', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.file:
            return '%s - %s' % (self.attraction.name, self.file)
        else:
            return '%s - %s' % (self.attraction.name, 'No Image!')


class ReviewImageFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='restaurant_review_image')
    file = models.FileField(upload_to='review_images/', help_text='Restaurant review image file.', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.file:
            return '%s - %s' % (self.user.username, self.file)
        else:
            return '%s - %s' % (self.user.username, 'No Image!')


class CommentImageFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_image')
    restaurant = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='attraction_comment_image')
    file = models.FileField(upload_to='comment_images/', help_text='Attraction comment image file.', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.file:
            return '%s - %s' % (self.attraction.name, self.file)
        else:
            return '%s - %s' % (self.attraction.name, 'No attachment')