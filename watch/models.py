import uuid
from django.db import models
from accounts_engine.models import BaseClass, CustomUser


class Video(BaseClass):
    """
    Model representing a video uploaded by an Admin.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    video_url = models.URLField(max_length=200)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title


class WatchEvent(BaseClass):
    """
    Model representing a watch event where a user watches a video.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watch_events')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watch_events')

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Watch Event'
        verbose_name_plural = 'Watch Events'

    def __str__(self):
        return f'{self.user.username} watched {self.video.title}'
