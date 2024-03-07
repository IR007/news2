from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('news_app.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

