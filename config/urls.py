from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('lawyerAccount/', include('lawyerAccount.urls')),
    path('helpline/', include('helpline.urls')),
    path('chatting/', include('chatting.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('debug', include(debug_toolbar.urls)),
    ]

