from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import MediaContent, Actor, Director, Genre, Award

index_name = 'mediacontents'


@registry.register_document
class MediaContentDocument(Document):
    actors = fields.NestedField(properties={
        'name': fields.TextField(),
    })
    director = fields.NestedField(properties={
        'name': fields.TextField(),
    })
    genre = fields.NestedField(properties={
        'name': fields.TextField(),
    })
    awards = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    class Index:
        name = index_name
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = MediaContent
        fields = [
            'title',
            'description',
            'video_url',
            'image_url',
            'subtitle',
            'content_type',
            'release_year',
        ]
        related_models = [Actor, Director, Genre, Award]
