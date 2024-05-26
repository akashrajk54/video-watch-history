from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
   path('admin/', admin.site.urls),
   path('auth/', include('accounts_engine.urls')),
   path('watch/', include('watch.urls'))
]

urlpatterns += staticfiles_urlpatterns()
