from django.urls import path
from .views import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path('', views.main, name="main"),
    path('lawyer_list/', views.main_lawyer_list, name='main_lawyer_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
