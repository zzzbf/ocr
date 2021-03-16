from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from demo.settings import DEBUG, STATIC_URL, STATICFILES_DIRS

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]
if not DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATICFILES_DIRS[0])
