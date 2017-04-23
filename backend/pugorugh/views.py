from bisect import bisect

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
    for age_pref in age_prefs.split(','):
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


class GetFilteredDog(RetrieveAPIView):
    '''
    View to get the next dog based on the user filter choice (undecided, liked
     or disliked).

    Only those undecided dogs that match user preferences are shown.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        user = self.request.user
        pk = int(self.kwargs.get('pk'))
        dog_filter = self.kwargs.get('dog_filter')

        if dog_filter == 'undecided':
            # Get size, gender and age of dogs the current user prefers.
            (size, gender, age) = models.UserPref.objects.filter(
                user=user
            ).values_list('size', 'gender', 'age')[0]

            # Convert the preferred age into the age query.
            age_ranges = classify_dog_age(age)
            age_query = create_dog_age_list(age_ranges)

            # Get the ids of all dogs liked and disliked by the current user.
            decided_dog_ids = models.Dog.objects.filter(
                userdog__user=user
            ).values_list('id', flat=True)

            # Get a list of ordered ids of all undecided dogs, which suit the
            # current user.
            filtered_dogs_ids = models.Dog.objects.exclude(
                id__in=decided_dog_ids
            ).filter(
                age__in=age_query,
                size__in=size.split(','),
                gender__in=gender.split(',')
            ).order_by('id').values_list('id', flat=True)

        elif dog_filter == 'liked':
            # Get ids of all dogs liked by the current user
            filtered_dogs_ids = models.Dog.objects.filter(
                userdog__user=user,
                userdog__status='l'
            ).order_by('id').values_list('id', flat=True)

        else:
            # Get ids of all dogs disliked by the current user
            filtered_dogs_ids = models.Dog.objects.filter(
                userdog__user=user,
                userdog__status='d'
            ).order_by('id').values_list('id', flat=True)

        # If there are filtered dogs
        if filtered_dogs_ids:
            # If pk is equal or greater than the highest filtered dog id
            if pk >= filtered_dogs_ids[len(filtered_dogs_ids) - 1]:
                # Send an imaginary Dog with the id of -1
                return models.Dog(
                    name=None,
                    image_filename=None,
                    breed=None,
                    age=None,
                    gender=None,
                    size=None,
                    id=-1
                )
            else:
                # Get the id of the next dog
                index = bisect(filtered_dogs_ids, pk)
                dog_id = filtered_dogs_ids[index]

            return get_object_or_404(self.get_queryset(), pk=dog_id)

        else:
            # If there are no filtered dogs
            raise Http404


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
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """View to get and update User Preferences."""
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


class IsStaff(RetrieveAPIView):
    """View to get whether the current user is staff or not."""
    serializer_class = serializers.StaffUserSerializer

    def get_object(self):
        return self.request.user
