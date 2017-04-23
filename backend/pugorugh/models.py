from django.contrib.auth.models import User
from django.db import models


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

    name = models.CharField(max_length=255, default='Buddy')
    image_filename = models.CharField(max_length=255, default='')
    breed = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=1)
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
    dog = models.ForeignKey(Dog, related_name='dogs')
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
    )

    def __str__(self):
        return self.user.username + ' - ' + self.dog.name + ' - ' + self.status


class UserPref(models.Model):
    user = models.ForeignKey(User)
    age = models.CharField(
        max_length=1,
        default='b,y,a,s'
    )
    gender = models.CharField(
        max_length=1,
        default='m,f'
    )
    size = models.CharField(
        max_length=2,
        default='s,m,l,xl'
    )

    def __str__(self):
        return self.user.username
