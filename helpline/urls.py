from django.urls import path

from helpline.views import views

app_name = 'helpline'

urlpatterns = [
    path('report/', views.report_main, name='report'),
    path('report/search/', views.report_search, name='report_search'),
    path('report/<int:pk>/new/', views.report_new, name='report_new'),
    path('report/new/lawyer-list/', views.report_lawyer_list,
         name='report_lawyer_list'),
    path('report/<uuid:pk>/confirm/', views.report_confirm, name='report_confirm'),
    path('report/result/', views.report_result, name='report_result'),
    path('report/<uuid:pk>/', views.report_detail, name='report_detail'),
    path('report/<uuid:pk>/reoffer/', views.report_reoffer, name='report_reoffer'),
    path('report/<uuid:pk>/checkKS/', views.report_checkKS, name='report_checkKS'),
    path('report/<uuid:pk>/check_log/', views.check_log, name='check_log'),
]

# 각 url 에 해당하는 view 에 주석을 통해 기능을 명시해두었습니다.
