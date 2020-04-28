from math import ceil

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from helpline.models import Report
from lawyerAccount.models import Lawyer
import hashlib


# main page(home page) view
def main(request):
    # 변호사 리스트와 변호사 랭킹을 위해 db 에 조회하여 저장
    lawyers = Lawyer.objects.exclude(rank=0).all().order_by('-rating') #rank=0인거(승인안받은 변호사)제외함
    lawyers_rank = lawyers.exclude(rank__in='0')[:5]
    context = {
        'lawyers': lawyers[:5],
        'lawyers_rank': lawyers_rank,
        'lawyer_count': Lawyer.objects.exclude(rank=0).count(),#rank=0인거(승인안받은 변호사)제외함
        'report_count': Report.objects.count(),
        'report_counting': Report.objects.filter(lawyer_ack="2").count(),
    }
    return render(request, 'core/main.html', context)


# main 페이지에서 변호사 리스트를 새로고침 없이 보여주기 위한 ajax 에서 호출하는 view
# helpline.views 에 있는 report_lawyer_list 함수와 동일
def main_lawyer_list(request):
    page = int(request.GET['page'])
    lawyers_queryset = Lawyer.objects.all().order_by(
        '-rating')[(page - 1) * 5:page * 5]
    lawyers = list(lawyers_queryset.values())
    page_count = Lawyer.objects.exclude(rank=0).count() #rank=0인거(승인안받은 변호사)제외함

    search = request.GET.get('search_lawyer', '')
    if search:
        lawyers_queryset = Lawyer.objects.exclude(rank=0).filter( #rank=0인거(승인안받은 변호사)제외함
            Q(name__icontains=search) | Q(speciality__name__icontains=search)
        ).distinct().order_by('-rating')[(page - 1) * 5:page * 5]
        lawyers = list(lawyers_queryset.values())
        page_count = Lawyer.objects.exclude(rank=0).filter( #rank=0인거(승인안받은 변호사)제외함
            Q(name__icontains=search) | Q(speciality__name__icontains=search)
        ).distinct().count()

    for i, lawyer in enumerate(lawyers_queryset):
        lawyers[i]['image'] = lawyer.image.url
        lawyers[i]['speciality'] = list(lawyer.speciality.all().values())

    context = {
        'lawyers': lawyers,
        'page_count': ceil(page_count / 5),
    }
    return JsonResponse(context)
