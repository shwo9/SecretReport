from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from math import ceil
import time
import datetime
from datetime import datetime

from helpline.models import Report, Author, Organization, ReportFile, Log
from helpline.secret.aes import AESCipher, make_aes_key
from helpline.secret.password import generate_password
from helpline.unique_key import make_unique_key
from helpline.secret.luniverse import *
from helpline.secret.keystore import *
from helpline.secret.keystore import _sha256
from lawyerAccount.models import Lawyer


import random
import hashlib
import json
import io


# report 의 첫 페이지 view(헬프라인 신고 메뉴에 해당)
def report_main(request):
    return render(request, 'helpline/report.html')


# 헬프라인 신고에서 기관명 검색 페이지에 해당하는 view
# 선택된 기관은 report_new view 의 두 번째 인자로 넘어감
def report_search(request):
    org = Organization.objects.all()
    # 사용자가 입력한 기관을 db 에서 조회하여 filtering 함
    search = request.GET.get('search', '')
    if search:
        org = org.filter(name__icontains=search).order_by('name')
    return render(request, 'helpline/report_search.html', {
        'org_list': org,
        'search': search,
    })


# 신고서 작성 view
def report_new(request, pk):
    lawyers = Lawyer.objects.exclude(rank=0).all().order_by(
        '-rating')[:5]  # rank=0인거(승인안받은 변호사)제외함
    organization = Organization.objects.get(pk=pk)
    if request.method == 'POST':
        # <--1차키 3등분하기
        reporter_seed = str(random.random())  # 2차 키 seed 랜덤 생성 블록에 올라감
        #reporter_seed = str(0.111)
        reporter_key2 = AESCipher(reporter_seed)  # 2차 키 생성

        key = make_aes_key()  # 1차 키 seed 생성
        reporter_key1 = AESCipher(key)  # 1차 키 생성
        enc_reporter_seed = reporter_key1.encrypt(
            reporter_seed)  # 1차 키로 2차 키 seed 암호화

        author_context = {
            'name': reporter_key2.encrypt(request.POST['name']),
            'identification_number': reporter_key2.encrypt(request.POST['rrn']),
            'address': reporter_key2.encrypt(request.POST['address']),
            'detail_address': reporter_key2.encrypt(request.POST['detail_address']),
            'phone_number': reporter_key2.encrypt(request.POST['phone']),
            'key': key
        }

        author = Author.objects.create(**author_context)

        data_seed = str(random.random())  # 2차 키 블록에 올라감
        #data_seed = str(0.111)
        data_key2 = AESCipher(data_seed)

        unique_key = make_unique_key()
        data_key1 = AESCipher(unique_key)
        enc_data_seed = data_key1.encrypt(data_seed)
        print(enc_data_seed, type(enc_data_seed))

        report_context = {
            'unique_key': unique_key,
            'author': author,
            'organization': organization,
            'title': request.POST['title'],
            'who': data_key2.encrypt(request.POST['who']),
            'when': data_key2.encrypt(request.POST['when']),
            'where': data_key2.encrypt(request.POST['where']),
            'content': data_key2.encrypt(request.POST['content']),
            'witness': data_key2.encrypt(request.POST['witness']),
            'method': data_key2.encrypt(request.POST['method']),
            'grasp': data_key2.encrypt(request.POST['grasp']),
            'term': data_key2.encrypt(request.POST['term']),
            'password': generate_password(request.POST['password']),
            'lawyer': Lawyer.objects.get(pk=request.POST['lawyer'])
        }
        report = Report.objects.create(**report_context)

        # Report 작성 시 등록한 첨부파일을 해당 Report 에 연결하여 저장
        for file in request.FILES.getlist('file'):
            ReportFile.objects.create(file=file, report=report)

        # function addReport(_id, _reporter, _reporterInfo, _desc, _RIkey, _DESCkey)
        report_hash = hashlib.sha256(report.unique_key.encode()).hexdigest()

        desc = hashReport(Report.objects.get(unique_key=unique_key))
        reporterInfo = hashAuthor(author)
        inputs = {"_id": CreateRptId(report.id), "_reporter": CreateRpterId(report.id), "_lawyer": CreateLawyerId(report.lawyer.id),
                  "_reporterInfo": str(reporterInfo), "_desc": str(desc),
                  "_RIkey": str(enc_reporter_seed), "_DESCkey": str(enc_data_seed), }
        sendDataToBC('ar9', inputs)  # 블록체인에 보내기

        # request.session['report_new'] 는 신고서 작성 완료시에만 True 로 변경되고,
        # 해당값이 True 일 때만 신고서 ID 발급 페이지에 접속 가능함
        # 신고서 작성 완료 후를 제외하고는 신고서 ID 발급 페이지에 접속할 수 없음
        request.session['report_new'] = True
        # 신고서 ID 발급 view 로 이동
        return redirect('helpline:report_confirm', report.pk)
    return render(request, 'helpline/report_new.html', {
        'organization': organization,
        'lawyers': lawyers,
        # rank=0인거(승인안받은 변호사)제외함
        'lawyer_count': Lawyer.objects.exclude(rank=0).count(),
        'page_count': ceil(lawyers.count() / 5)
    })


# 신고서 작성 페이지에서 변호사 리스트를 새로고침 없이 보여주기 위한 ajax 에서 호출하는 view
# 변호사 재신청 페이제의 경우도 해당 view 를 사용함


def report_lawyer_list(request):
    # 변호사 list 의 pagination 구현을 위한 변수
    page = int(request.GET['page'])
    # 변호사의 list 를 db 에서 가져온 후,
    # list 로 만들어 lawyers 에 저장(json 으로 넘겨줘야하기 때문에 list 로 만들어야함)
    # 변호사 list 가 몇 페이지로 구현되는지 파악하기 위해 page_count 변수에 저장
    lawyers_queryset = Lawyer.objects.exclude(rank=0).all().order_by(  # rank=0인거(승인안받은 변호사)제외함
        '-rating')[(page - 1) * 5:page * 5]
    lawyers = list(lawyers_queryset.values())
    page_count = Lawyer.objects.count()

    # 검색어(변호사 이름 or 전문분야)가 있을 경우
    search = request.GET.get('search_lawyer', '')
    if search:
        # 검색어에 해당하는 값을 가진 변호사 정보들을 db 에 조회하여 저장
        lawyers_queryset = Lawyer.objects.exclude(rank=0).filter(  # rank=0인거(승인안받은 변호사)제외함
            Q(name__icontains=search) | Q(speciality__name__icontains=search)
        ).distinct().order_by('-rating')[(page - 1) * 5:page * 5]
        lawyers = list(lawyers_queryset.values())
        page_count = Lawyer.objects.exclude(rank=0).filter(  # rank=0인거(승인안받은 변호사)제외함
            Q(name__icontains=search) | Q(speciality__name__icontains=search)
        ).distinct().count()

    # 변호사 image url 과 speciality(전문분야)는 json response 를 위해 값을 변경시켜줌
    for i, lawyer in enumerate(lawyers_queryset):
        lawyers[i]['image'] = lawyer.image.url
        lawyers[i]['speciality'] = list(lawyer.speciality.all().values())

    context = {
        'lawyers': lawyers,
        'page_count': ceil(page_count / 5),
    }
    return JsonResponse(context)


# 발급된 신고서 ID 를 보여주는 view
@csrf_exempt
def report_confirm(request, pk):

    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        # salt만들기
        randomNumber = str(random.random())
        salt = _sha256(randomNumber)
        password = request.POST['password3']
        report_hash = _sha256(report.unique_key)
        mac = _sha256(salt+password)
        keystore = {"id": report_hash, "salt": salt, "mac": mac}
        text = json.dumps(keystore)
        response = HttpResponse(text, content_type='txt/plain')
        response['Content-Disposition'] = 'attachment; filename= keystore'

        return response

    # 신고서 작성을 완료하지 않고 해당 url 로 접속하면 PermissionDenied 오류 발생
    if not request.session.get('report_new', False):
        raise PermissionDenied
    # 발급된 신고서 ID 는 한 번만 보여줘야하기 때문에 이후 접속을 막기 위해 False 로 바꿔줌
    request.session['report_new'] = False

    return render(request, 'helpline/report_confirm.html', {
        'report': report,
    })


# 신고내역 확인을 위한 view(신고내역 확인 메뉴에 해당)
@csrf_exempt
def report_result(request):
    unique_key = ''
    if request.method == 'POST':
        # 신고서 ID, 비밀번호 미입력 or 비밀번호 미입력 or 해당 신고서 존재 여부 판단
        try:
            unique_key = request.POST.get('unique_key', '')
            # 신고서 ID 를 입력하지 않았을 경우 오류 발생
            if not unique_key:
                raise ValueError("신고서 ID를 입력해주세요.")
            password = request.POST.get('password', '')
            # 비밀번호를 입력하지 않았을 경우 오류 발생
            if not password:
                raise ValueError("비밀번호를 입력해주세요.")
            report = Report.objects.get(
                unique_key=unique_key, password=generate_password(password))
            # 해당하는 신고서를 찾았을 경우 신고서 상세 페이지로 이동
            # 이 경우 request.session['confirm'] 는 True 로 변경되고,
            # 신고서 상세 페이지로 접속할 수 있음
            return redirect('helpline:report_checkKS', report.pk)
        except ValueError as e:
            messages.error(request, e)
        # 입력한 신고서 ID 와 비밀번호와 맞는 신고서가 존재하지 않을 경우 오류 발생
        except Report.DoesNotExist:
            messages.error(request, '신고서 ID 또는 비밀번호를 다시 확인하세요.')
    return render(request, 'helpline/report_result.html', {
        'unique_key': unique_key,
    })


# 신고서 상세 페이지 view
@csrf_exempt
def report_detail(request, pk):
    # 신고서 ID 와 비밀번호 입력 or 변호사 재신청을 제외한 다른 방법으로 해당 url 로 접속하면
    # 신고내역 확인 페이지(신고서 ID, 비밀번호 입력)으로 이동시킴
    report = Report.objects.get(pk=pk)
    if request.method == 'POST':
        request.session['log_confirm'] = True
        return redirect('helpline:check_log', report.pk)

    if not request.session.get('confirm', False):
        return redirect('helpline:report_result')
    # 예외를 막기 위해 request.session['confirm'] 을 False 로 변경
    # 따라서 페이지 리로드 시, 신고내역 확인 페이지로 이동되어 신고서 ID, 비밀번호를 재입력해야 함
    # request.session['confirm'] = False

    # 해당하는 신고서를 db 에서 조회 후,
    # 신고서의 신고서 ID를 이용하여 복호화(aes_report.decrypt(...)) 과정을 거침
    report_hash = hashReport(report)
    inputs = {"_id": CreateRptId(report.id), "_user": CreateRpterId(
        report.id), "_hashedData": report_hash}
    txId = sendDataToBC('dk9', inputs)
    seed = ''
    if txId:
        res = getDataFromBC(txId)

    key1 = AESCipher(report.unique_key)
    if res:
        seed = res['log']['msg']
        log_context = {
            'report': report,
            'timestamp': datetime.fromtimestamp(int(res['log']['_time'])),
            'txHash': res['txHash'],
            'user': res['log']['user']
        }
        log = Log.objects.create(**log_context)
        key2 = key1.decrypt(seed)
        print('blockchain seed : ', key2)
    if not seed:
        key2 = '0.111'
        print('default seed : ', key2)

    #aes_report = AESCipher(report.unique_key)
    aes_report = AESCipher(key2)

    log_list = Log.objects.filter(report=report)

    logs = {
        log: {
            'user': log.user,
            'timestamp': log.timestamp,
            'txhash': log.txHash,
        }
        for log in log_list
    }

    report_context = {
        'report': report,
        'report_title': report.title,
        'report_who': aes_report.decrypt(report.who),
        'report_when': aes_report.decrypt(report.when),
        'report_where': aes_report.decrypt(report.where),
        'report_content': aes_report.decrypt(report.content),
        'report_witness': aes_report.decrypt(report.witness),
        'report_method': aes_report.decrypt(report.method),
        'report_grasp': aes_report.decrypt(report.grasp),
        'report_term': aes_report.decrypt(report.term),
        'report_lawyer_ack': report.get_lawyer_ack_display(),
        'logs': logs,
    }

    return render(request, 'helpline/report_detail.html', report_context)


def report_checkKS(request, pk):
    print('test')
    if request.method == 'POST':
        report = get_object_or_404(Report, pk=pk)
        password = request.POST['pw']
        f = request.FILES['keystore']
        print(f)

        str_KS = f.readline()
        dict_KS = json.loads(str_KS)
        report_hash1 = _sha256(report.unique_key)
        report_hash2 = dict_KS['id']
        salt = dict_KS['salt']
        seed = salt+password
        mac1 = _sha256(seed)
        mac2 = dict_KS['mac']
        if report_hash1 != report_hash2:
            messages.error(request, '잘못된 키스토어입니다.')
        elif mac1 != mac2:
            messages.error(request, '틀린 비밀번호입니다.')
        else:
            request.session['confirm'] = True
            return redirect(report)

    return render(request, 'helpline/report_checkKS.html')

# 변호사 재신청(수임요청 거절 시) view


@csrf_exempt
def report_reoffer(request, pk):
    report = get_object_or_404(Report, pk=pk)
    lawyers = Lawyer.objects.exclude(rank=0).all().order_by('-rating')[:5]
    # 수임요청이 거절되지 않았으나 해당 url 로 접근시 신고내역 확인 페이지로 이동
    if report.lawyer:
        return redirect(report)
    if request.method == "POST":
        report.lawyer = Lawyer.objects.get(pk=request.POST['lawyer'])
        inputs = {"_id": CreateRptId(
            report.id), "_lawyer": CreateLawyerId(report.lawyer.id)}
        sendDataToBC('al9', inputs)
        report.lawyer_ack = '1'
        report.save()
        # 변호사 재신청 과정 완료 후,
        # request.session['confirm'] = True 로 변경한 후,
        # 신고내역 상세 페이지로 이동
        request.session['confirm'] = True
        return redirect("helpline:report_detail", pk)
    return render(request, 'helpline/report_reoffer.html', {
        'report': report,
        'lawyers': lawyers,
        'lawyer_count': Lawyer.objects.exclude(rank=0).count(),
        'page_count': ceil(lawyers.count() / 5)
    })


def check_log(request, pk):
    # if not request.session.get('log_confirm', False):
    #     return redirect('helpline:report_result')

    # request.session['log_confirm'] = False
    report = get_object_or_404(Report, pk=pk)
    log_list = Log.objects.filter(report=report)

    logs = {
        log: {
            'user': log.user,
            'timestamp': log.timestamp,
            'txhash': log.txHash,
        }
        for log in log_list
    }

    return render(request, 'helpline/check_log.html', {
        'report_title': report.title,
        'logs': logs
    })
