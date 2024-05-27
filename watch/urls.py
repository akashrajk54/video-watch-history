from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, WatchEventViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'watch', WatchEventViewSet, basename='watch')

urlpatterns = [
    path('', include(router.urls)),
]
