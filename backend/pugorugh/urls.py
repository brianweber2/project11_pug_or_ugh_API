from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import UserRegisterView, GetFilteredDog, IsStaff

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='next_dog'),
    url(
        r'^api/dog/(?P<pk>-?\d+)/(?P<dog_filter>liked|disliked|undecided)/next/$',
        GetFilteredDog.as_view(),
        name='filtered-dog-detail'),
    url(r'^api/user/isstaff/$', IsStaff.as_view(), name='user-is-staff'),
])
