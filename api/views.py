from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )




class MovieViewSet(viewsets.ModelViewSet):
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )



    @action(detail=True, methods=["POST"])
    def rate_movie(self, request, pk=None):
        movie = models.Movie.objects.get(id=pk)
        stars = request.data['stars']
        user = request.user
        # user = User.objects.get(id=1)
        if 'stars' in request.data:
            try:
                rating = models.Rating.objects.get(user=user, movie=movie)
                rating.stars = stars
                rating.save()
                serializers = RatingSerializer(rating, many=False)
                response = {'message': "Rating Updated", 'result':serializers.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating=models.Rating.objects.create(user=user, movie=movie, stars=stars)
                serializers = RatingSerializer(rating, many=False)
                response = {'message': "Rating Created", 'result': serializers.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = models.Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        response = {'message': "You can't update like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        response = {'message': "You can't create like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)




