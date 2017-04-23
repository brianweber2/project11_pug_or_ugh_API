from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Dog(models.Model):
    """Dog model class."""
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

    name = models.CharField(max_length=255, default='Unknown name')
    image_filename = models.CharField(max_length=255, default='')
    breed = models.CharField(max_length=255, default='Unknown mix')
    age = models.IntegerField(default=1)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='Unknown gender'
    )
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        default='Unknown size'
    )
    neutered = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """User's Dog decision model class."""
    STATUS_CHOICES = (
        ('l', 'liked'),
        ('d', 'disliked'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
    )

    def __str__(self):
        return self.user.username + ' - ' + self.dog.name + ' - ' + self.status


class UserPref(models.Model):
    """User Preference model class."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(
        max_length=7,
        default='b,y,a,s'
    )
    gender = models.CharField(
        max_length=3,
        default='m,f'
    )
    size = models.CharField(
        max_length=8,
        default='s,m,l,xl'
    )

    def __str__(self):
        return self.user.username


def create_userpref(sender, **kwargs):
    """Create UserPref isntance whenever User is created."""
    user = kwargs['instance']
    if kwargs['created']:
        user_pref = UserPref(user=user)
        user_pref.save()

post_save.connect(create_userpref, sender=User)
