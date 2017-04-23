from django.contrib.auth import get_user_model
from django.shortcuts import Http404, get_object_or_404
from django.db.models import Q

from rest_framework import permissions
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response

from . import serializers
from . import models

def classify_dog_age(age_prefs):
    age_filter = {}
    for age_pref in age_prefs:
        if age_pref == 'b':
            age_filter['b'] = range(0, 12)
        elif age_pref == 'y':
            age_filter['y'] = range(12, 24)
        elif age_pref == 'a':
            age_filter['a'] = range(24, 72)
        elif age_pref == 's':
            age_filter['s'] = range(72, 200)
    return age_filter

def create_dog_age_list(age_ranges):
    age_range_list = []
    for age_range in age_ranges.values():
        for x in age_range:
            age_range_list.append(x)
    return age_range_list

class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class GetNextDog(RetrieveAPIView):
    '''
    Grabs the next liked, disliked or undecided dog.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def _filter_on_preferences(self, dog_filter, user_prefs):
        age_prefs = user_prefs.age.split(',')
        gender_prefs = user_prefs.gender
        size_prefs = user_prefs.size

        age_ranges = classify_dog_age(age_prefs)
        age_range_list = create_dog_age_list(age_ranges)

        if dog_filter == 'liked':
            query_filter = 'l'
        elif dog_filter == 'disliked':
            query_filter = 'd'
        elif dog_filter == 'undecided':
            query_filter = 'u'
        else:
            raise Http404

        if query_filter == 'u':
            dog_pks_to_exclude = []
            user_dogs = models.UserDog.objects.filter(user=self.request.user)

            for user_dog in user_dogs:
                dog_pks_to_exclude.append(user_dog.dog.pk)

            dogs = models.Dog.objects.filter(
                age__in=age_range_list,
                gender__in=gender_prefs,
                size__in=size_prefs,
            ).exclude(pk__in=dog_pks_to_exclude)
            return dogs
        elif query_filter == 'l':
            user_dogs = models.UserDog.objects.filter(
                user=user_prefs.user,
                status='l'
            )
            return user_dogs
        elif query_filter == 'd':
            user_dogs = models.UserDog.objects.filter(
                user=user_prefs.user,
                status='d'
            )
            return user_dogs

    def get_queryset(self):
        user = self.request.user
        dog_filter = self.kwargs.get('dog_filter')
        # Get user preferences
        user_prefs = get_object_or_404(models.UserPref, user=user)
        # Get dogs based on user preference selections
        queryset = self._filter_on_preferences(dog_filter, user_prefs)
        return queryset

    def get_object(self):
        pk = self.kwargs.get('pk')
        print(pk)
        try:
            pk = int(pk)
        except:
            raise Http404
        dog_filter = self.kwargs.get('dog_filter')

        # Filter the query for the NEXT dog by pk
        if dog_filter == 'undecided':
            queryset = self.get_queryset().filter(pk__gt=pk)
            obj = queryset.first()
        else:
            queryset = self.get_queryset().filter(dog__pk__gt=pk)
            obj = queryset.first().dog
        if not obj:
            raise Http404
        return obj


class DogViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

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
    mixins.CreateModelMixin,
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
        user_pref = models.UserPref.objects.get(user=user)

        if request.method == 'PUT':
            data = request.data
            user_pref.age = data.get('age')
            user_pref.gender = data.get('gender')
            user_pref.size = data.get('size')
            user_pref.save()

        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data)

