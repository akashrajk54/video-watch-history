from django.urls import path, include
from rest_framework import routers
from .views import MediaContentSearchView

router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('content/', MediaContentSearchView.as_view(), name='media_content_search'),
]
