from rest_framework import serializers
from .models import MediaContent, Actor, Director, Genre, Award


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name']


class MediaContentSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    awards = AwardSerializer(read_only=True, allow_null=True)
    content_type = serializers.CharField(source='get_content_type_display')

    class Meta:
        model = MediaContent
        fields = [
            'id', 'title', 'description', 'video_url', 'image_url',
            'subtitle', 'content_type', 'release_year', 'actors',
            'director', 'genre', 'awards', 'created_date', 'updated_date'
        ]
