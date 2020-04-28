from django.urls import path, re_path
from .views import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "lawyerAccount"

urlpatterns = [

    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signup/id_overlap_check',
         views.id_overlap_check, name="id_overlap_check"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('find_id/', views.find_id, name="find_id"),
    path('find_password/', views.find_password, name="find_password"),
    path('change_password/<int:user_id>',
         views.change_password, name="change_password"),

    path('mypage/<int:user_id>/', views.mypage, name="mypage"),
    path('mypage/<int:user_id>/lawyer_edit',
         views.lawyer_edit, name="lawyer_edit"),
    path('report_page/<uuid:report_id>', views.report_page, name="report_page"),
    path('report_page/<uuid:report_id>/lawyer_ack',
         views.lawyer_ack, name="lawyer_ack"),
    path('report_page/<uuid:report_id>/lawyer_refuse',
         views.lawyer_refuse, name="lawyer_refuse"),
    # TODO: 변호사 세부 페이지 url 변경
    path('lawyer_info/', views.lawyer_info, name="lawyer_info"),
    path('report_page/<int:user_id>/checkKS/', views.checkKS, name="checkKS"),
    path('report_page/<int:user_id>/downloadKS/',
         views.downloadKS, name="downloadKS"),
    #path('report_page/<int:user_id>/newKS/', views.newKS, name="newKS")
    path('report_page/<uuid:report_id>/reporter',
         views.reporterInfo, name="reporterInfo"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
