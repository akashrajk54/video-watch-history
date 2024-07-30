from django.contrib import admin
from watch.models import (Video, WatchEvent)

# Register models here.
admin.site.register(Video)
admin.site.register(WatchEvent)
