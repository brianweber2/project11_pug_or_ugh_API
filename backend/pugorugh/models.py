from django.contrib.auth.models import User
from django.db import models

from multiselectfield import MultiSelectField


class Dog(models.Model):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('u', 'unknown'),
    )
    SIZE_CHOICES = (
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large'),
        ('u', 'unknown'),
    )

    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default='')
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='m'
    )
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        default='s'
    )

    def __str__(self):
        return self.name


class UserDog(models.Model):
    STATUS_CHOICES = (
        ('l', 'liked'),
        ('d', 'disliked'),
    )

    user = models.ForeignKey(User, null=True)
    dog = models.ForeignKey(Dog)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return self.user.username + ' - ' + self.dog.name + ' - ' + self.status


class UserPref(models.Model):
    AGE_CHOICES = (
        ('b', 'baby'),
        ('y', 'young'),
        ('a', 'adult'),
        ('s', 'senior'),
    )
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )
    SIZE_CHOICES = (
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large'),
    )

    user = models.ForeignKey(User)
    age = MultiSelectField(
        max_length=1,
        choices=AGE_CHOICES,
        default='b',
        max_choices=4
    )
    gender = MultiSelectField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='m',
        max_choices=2
    )
    size = MultiSelectField(
        max_length=2,
        choices=SIZE_CHOICES,
        default='s',
        max_choices=4
    )

    def __str__(self):
        return self.user.username
