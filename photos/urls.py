from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from photos.views import Logout, GroupViewSet, ImageViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'photos', ImageViewSet)

urlpatterns = [
        url('', include(router.urls)),
        url(r'^login/$', obtain_auth_token),
        url(r'^logout/$', Logout.as_view()),
]
