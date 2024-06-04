from django.db import models
from django.utils.translation import gettext_lazy as _


class Actor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Award(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Award'
        verbose_name_plural = 'Awards'


class MediaContent(models.Model):
    class ContentType(models.TextChoices):
        MOVIE = 'MV', _('Movie')
        TV_SHOW = 'TV', _('TV Show')
        DOCUMENTARY = 'DC', _('Documentary')
        OTHER = 'OT', _('Other')

    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    image_url = models.URLField()
    subtitle = models.TextField()
    content_type = models.CharField(
        max_length=2,
        choices=ContentType.choices,
        default=ContentType.OTHER,
    )
    release_year = models.IntegerField()
    actors = models.ManyToManyField(Actor, related_name='media_contents')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='media_contents')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='media_contents')
    awards = models.ForeignKey(Award, null=True, blank=True, on_delete=models.SET_NULL, related_name='media_contents')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Media Content'
        verbose_name_plural = 'Media Contents'
