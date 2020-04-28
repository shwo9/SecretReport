from django.urls import path,re_path
from .views import views
from django.conf import settings
from django.conf.urls.static import static

# test
from django.conf.urls import url


app_name = "chatting"

urlpatterns = [
    # 재원님이 아직 report_id로 넘길지 뭘로 넘길지 못정하셨다. 
    path('room/<uuid:report_id>/', views.enter_chatting_room, name="enter_chatting_room"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

