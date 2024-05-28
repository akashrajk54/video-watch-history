from django.urls import path, include
from rest_framework import routers
from watch.views import VideoViewSet, WatchEventViewSet, Home

router = routers.SimpleRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'watch', WatchEventViewSet, basename='watch')

urlpatterns = [
    path('', Home, name='home'),
    path('', include(router.urls)),
]
