from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^accounts/', include('accounts.urls')),  # does the same as root url
    url(r'^article/', include('article.urls')),   # handles article requests
    url(r'^uliza/', include('uliza.urls')),   # handles article requests
    url(r'^admin/', admin.site.urls),  # admins site url

    # root url, do not put any url after this, put all your new urls above
    url(r'^', include('accounts.urls')),
]

if settings.DEBUG:
    # this url handles the media uploaded on the site
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # this url handles the static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
