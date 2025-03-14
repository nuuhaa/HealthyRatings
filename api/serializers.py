from rest_framework import serializers, status
from .models import Product, Rating

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'no_of_ratings', 'avg_rating')  # Updated to reference Product

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'user', 'product')  # Updated to reference Product