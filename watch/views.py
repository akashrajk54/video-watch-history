from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view

from watch.models import Video, WatchEvent
from accounts_engine.custom_pagination import CustomPagination
from watch.serializers import VideoSerializer, WatchEventSerializer
from accounts_engine.utils import success_true_response, success_false_response
import logging

logger = logging.getLogger(__name__)
logger_info = logging.getLogger('info')
logger_error = logging.getLogger('error')


@api_view(['GET'])
def Home(request):
    return Response({'success': True})


class VideoViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Video.objects.all().order_by('-created_date')
    serializer_class = VideoSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['=id', '$title']
    ordering_fields = ['id', 'title']
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super(VideoViewSet, self).get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ['list', 'retrieve']:
            context['exclude_user'] = True
        return context

    def get_queryset(self):
        if self.action == 'list':
            sorted_queryset = Video.objects.all().order_by('-created_date')
            return sorted_queryset

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_admin:
                message = 'Only admins can upload videos.'
                logger_error.error(message)
                return Response(success_false_response(message=message), status=status.HTTP_403_FORBIDDEN)

            requested_data = request.data.copy()
            requested_data['user'] = user.id
            serializer = self.get_serializer(data=requested_data)

            try:
                serializer.is_valid(raise_exception=True)
                video = serializer.save(user=user)
                message = 'Video uploaded successfully.'
                logger_info.info(f'{message} by {user.username}')
                return Response(success_true_response(data={'id': video.id}, message=message), status=status.HTTP_201_CREATED)

            except ValidationError as e:
                error_detail = e.detail
                for field_name, errors in error_detail.items():
                    for error in errors:
                        message = str(error)
                        logger_error.error(message)
                        return Response(success_false_response(message=message), status=e.status_code)

        except Exception as e:
            message = str(e)
            logger_error.error(message)
            return Response(success_false_response(message='An unexpected error occurred. Please try again later.'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger_info.info('All videos retrieved successfully.')
                return self.get_paginated_response(data=serializer.data)

            videos = Video.objects.all().order_by('-created_date')
            serializer = self.get_serializer(videos, many=True)
            message = 'All videos retrieved successfully.'
            logger_info.info(message)
            return Response(success_true_response(data=serializer.data, message=message))
        except Exception as e:
            message = str(e)
            logger_error.error(message)
            return Response(success_false_response(message='An unexpected error occurred. Please try again later.'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchEventViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = WatchEventSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['=id', '$video__title']
    ordering_fields = ['id', 'video__title']
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ['watch_history']:
            context['exclude_user'] = True
        # Set depth for GET requests
        if self.request.method == 'GET':
            context['depth'] = 1
        else:
            context['depth'] = 0
        return context

    def get_queryset(self):
        if self.action == 'watch_history':
            user = self.request.user
            limit = self.request.query_params.get('limit')
            offset = self.request.query_params.get('offset')
            start_date_str = self.request.query_params.get('start_date')
            end_date_str = self.request.query_params.get('end_date')

            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(
                    seconds=1)
                queryset = WatchEvent.objects.filter(user=user, is_delete=False, created_date__range=[start_date, end_date])
            else:
                queryset = WatchEvent.objects.filter(user=user, is_delete=False)

            cache_key = f'watch_history_{user.id}_limit={limit}_offset={offset}_start={start_date_str}_end={end_date_str}'
            cached_queryset = cache.get(cache_key)

            if cached_queryset is not None:
                message = 'Watch history retrieved from cache successfully.'
                logger_info.info(message)
                return cached_queryset

            cache.set(cache_key, queryset, timeout=300)

            # Add cache_key to the user's cache list
            cache_key_list = cache.get(f'cache_keys_{user.id}', [])
            cache_key_list.append(cache_key)
            cache.set(f'cache_keys_{user.id}', cache_key_list, timeout=300)

            return queryset

    def create(self, request, *args, **kwargs):
        try:

            user = request.user
            requested_data = request.data.dict()
            requested_data['user'] = user.id

            video_id = requested_data.get('video')
            if not Video.objects.filter(id=video_id).exists():
                message = f'Video with id {video_id} does not exist.'
                logger_error.error(message)
                return Response(success_false_response(message='Video not found. Please try some other.'), status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=requested_data)

            try:
                serializer.is_valid(raise_exception=True)
                video_watched = serializer.save(user=user)

                # Invalidate the cache for watch history
                self.invalidate_watch_history_cache(user.id)
                logger_info.info(f'Cache invalidated for {user.username}')

                message = 'Watch event created successfully.'
                logger_info.info(f'{message} for {user.username}')

                return Response(success_true_response(data={'id': video_watched.id}, message=message), status=status.HTTP_201_CREATED)

            except ValidationError as e:
                error_detail = e.detail
                for field_name, errors in error_detail.items():
                    for error in errors:
                        message = str(error)
                        logger_error.error(message)
                        return Response(success_false_response(message=message), status=e.status_code)

        except Exception as e:
            message = str(e)
            logger_error.error(message)
            return Response(success_false_response(message='An unexpected error occurred. Please try again later.'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def invalidate_watch_history_cache(self, user_id):
        """ Invalidate cache keys for the watch history of a user. """
        cache_key_list = cache.get(f'cache_keys_{user_id}', [])
        for key in cache_key_list:
            logger_info.info(f'Deleting cache key: {key}')
            cache.delete(key)
        cache.delete(f'cache_keys_{user_id}')

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def watch_history(self, request):
        try:

            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger_info.info('Watch history retrieved successfully.')
                return self.get_paginated_response(data=serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            message = 'Watch history retrieved successfully.'
            logger_info.info(message)
            return Response(success_true_response(data=serializer.data, message=message))
        except Exception as e:
            message = str(e)
            logger_error.error(message)
            return Response(success_false_response(message='An unexpected error occurred. Please try again later.'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
