from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}} # for hiding password

    def create(self, validated_data): # for creating hashed password
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ['id', 'title', 'description', 'no_of_ratings', 'avg_rating']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ['id', 'movie', 'user', 'stars']
