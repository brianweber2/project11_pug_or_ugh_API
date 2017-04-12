from django.contrib import admin

# Register your models here.
from .models import Dog, UserDog, UserPref


admin.site.register(Dog)
admin.site.register(UserDog)
admin.site.register(UserPref)
