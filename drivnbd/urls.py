from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("products/", include("store.urls")),
    path("api/v1", include("api.urls")),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
