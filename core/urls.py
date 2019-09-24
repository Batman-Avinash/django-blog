from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path

urlpatterns = [
	path('', include('home.urls')),
	path('blog/', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)