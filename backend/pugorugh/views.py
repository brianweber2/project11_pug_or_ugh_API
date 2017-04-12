from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import serializers
from . import models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    # /api/dog/<pk>/liked/next/
    @detail_route(methods=['get'], url_path='liked/next')
    def liked_next(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog = models.UserDog.objects.get(user=user, dog=dog)
        if user_dog.status == 'l':
            serializer = serializers.DogSerializer(user_dog.dog)
            return Response(serializer.data)
        else:
            return Response(404)


    # /api/dog/<pk>/disliked/next/
    @detail_route(methods=['get'], url_path='disliked/next')
    def disliked_next(self, request, pk=None):
        pass

    # /api/dog/<pk>/undecided/next/
    @detail_route(methods=['get'], url_path='undecided/next')
    def undecided_next(self, request, pk=None):
        pass

    # /api/dog/<pk>/liked/
    @detail_route(methods=['post', 'put'])
    def liked(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog, created = models.UserDog.objects.get_or_create(
            user=user, dog=dog
        )
        user_dog.status = 'l'
        user_dog.save()
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)

    # /api/dog/<pk>/diksliked/
    @detail_route(methods=['post', 'put'])
    def disliked(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog, created = models.UserDog.objects.get_or_create(
            user=user, dog=dog
        )
        user_dog.status = 'd'
        user_dog.save()
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)

    # /api/dog/<pk>/undecided/
    @detail_route(methods=['post', 'put'])
    def undecided(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog, created = models.UserDog.objects.get_or_create(
            user=user, dog=dog
        )
        user_dog.status = 'u'
        user_dog.save()
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)


class UserPrefViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    # /api/user/preferences/
    @detail_route(methods=['get', 'put'])
    def preferences(self, request, pk=None):
        pass

