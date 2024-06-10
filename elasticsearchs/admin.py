from django.contrib import admin
from elasticsearchs.models import Actor, Director, Genre, Award, MediaContent

admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Award)
admin.site.register(MediaContent)

