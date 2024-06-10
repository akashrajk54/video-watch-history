from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
   path('admin/', admin.site.urls),
   path('auth/', include('accounts_engine.urls')),
   path('', include('watch.urls')),
   path('search/', include('elasticsearchs.urls')),
]

urlpatterns += staticfiles_urlpatterns()
