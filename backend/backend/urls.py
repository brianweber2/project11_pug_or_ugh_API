from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken import views

from pugorugh import views as pugorugh_views

router = routers.SimpleRouter()
router.register(r'dog', pugorugh_views.DogViewSet)
router.register(r'user', pugorugh_views.UserPrefViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('pugorugh.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api/', include(router.urls, namespace='api'))
]
