# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers

from foosball.api.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]