from django.contrib.auth import get_user_model
from django.shortcuts import Http404, get_object_or_404

from rest_framework import permissions
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
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

    def _filter_on_preferences(self, dog_filter, user_prefs):
        pass

    def get_filtered_queryset(self):
        user =  self.request.user
        dog_filter = self.kwargs.get('dog_filter')
        print(dog_filter)
        # Get user preferences
        user_prefs = get_object_or_404(models.UserPref, user=user)
        # Get age ranges(months) based on user preference selections
        queryset = self._filter_on_preferences(dog_filter, user_prefs)
        return queryset

    def get_next_object(self):
        pk = int(self.kwargs.get('pk'))
        queryset = self.get_filtered_queryset().filter(pk__gt=pk)
        obj = queryset.first()
        if not obj:
            raise Http404
        return obj

    # /api/dog/<pk>/liked/next/
    @detail_route(methods=['get'], url_path='liked/next')
    def liked_next(self, request, pk=None):
        user = request.user
        dog = self.get_next_object()

        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)

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
    @list_route(methods=['get', 'put'])
    def preferences(self, request, pk=None):
        user = request.user
        data = request.data
        user_pref, created = models.UserPref.objects.get_or_create(
            user=user
        )

        if request.method == 'PUT':
            user_pref.age = data.get('age')
            user_pref.gender = data.get('gender')
            user_pref.size = data.get('size')
            user_pref.save()

        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data)

