from django.core.management.base import BaseCommand
from elasticsearchs.models import MediaContent
from elasticsearchs.search import VideoDocument

class Command(BaseCommand):
    help = 'Index data into Elasticsearch'

    def handle(self, *args, **kwargs):
        videos = MediaContent.objects.all()
        for video in videos:
            video_doc = VideoDocument(
                meta={'id': video.id},
                title=video.title,
                description=video.description,
                video_url=video.video_url,
                image_url=video.image_url,
                subtitle=video.subtitle,
                content_type=video.content_type,
                release_year=video.release_year,
                actors=[actor.name for actor in video.actors.all()],
                director=video.director.name,
                genre=video.genre.name,
                awards=video.awards.name if video.awards else None
            )
            video_doc.save()
        self.stdout.write(self.style.SUCCESS('Data indexed successfully'))
