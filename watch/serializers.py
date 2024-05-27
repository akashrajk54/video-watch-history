from rest_framework import serializers
from .models import Video, WatchEvent


class VideoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'user', 'title', 'description', 'video_url', 'created_date', 'updated_date']
        read_only_fields = ['id', 'created_date', 'updated_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_user'):
            representation.pop('user')
        return representation


class WatchEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchEvent
        fields = ['id', 'user', 'video', 'created_date', 'updated_date']
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        if context.get('depth', None):
            self.Meta.depth = context['depth']
        else:
            self.Meta.depth = 0
        super(WatchEventSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_user'):
            representation.pop('user')
            representation['video'].pop('user', None)
            representation['video'].pop('is_delete', None)
            representation['video'].pop('deleted_date', None)
        return representation
