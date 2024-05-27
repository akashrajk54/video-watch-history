from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from watch.models import Video, WatchEvent
from accounts_engine.custom_pagination import CustomPagination
from watch.serializers import VideoSerializer, WatchEventSerializer
from accounts_engine.utils import success_true_response, success_false_response
import logging

logger = logging.getLogger(__name__)
logger_info = logging.getLogger('info')
logger_error = logging.getLogger('error')


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
            return Response(success_false_response(message='Internal server error'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response(success_false_response(message='Internal server error'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchEventViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = WatchEvent.objects.all().order_by('-created_date')
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
            sorted_queryset = self.queryset.filter(user=user, is_delete=False).order_by('-created_date')
            return sorted_queryset

    def create(self, request, *args, **kwargs):
        try:

            user = request.user
            requested_data = request.data.dict()
            requested_data['user'] = user.id
            logger_info.info(f'Request data: {requested_data}')

            video_id = requested_data.get('video')
            if not Video.objects.filter(id=video_id).exists():
                message = f'Video with id {video_id} does not exist.'
                logger_error.error(message)
                return Response(success_false_response(message=message), status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=requested_data)

            try:
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user)
                message = 'Watch event logged successfully.'
                logger_info.info(f'{message} for {user.username}')
                # Serialize the Video object before returning it in the response
                video_instance = Video.objects.get(id=requested_data['video'])
                video_serializer = VideoSerializer(video_instance)
                video_data = video_serializer.data
                # Remove the 'user' field from the serialized video data
                video_data.pop('user')

                return Response(success_true_response(data=video_data, message=message), status=status.HTTP_201_CREATED)

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
            return Response(success_false_response(message='Internal server error'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response(success_false_response(message='Internal server error'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

