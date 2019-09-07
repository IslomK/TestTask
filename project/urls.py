from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from apps.restful.urls import urlpatterns

schema_view = get_swagger_view(title='Bozor.com', url='/v1/', patterns=urlpatterns)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    path('v1/', include('apps.restful.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
