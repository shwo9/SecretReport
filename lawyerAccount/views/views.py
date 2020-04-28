from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from helpline.secret.aes import AESCipher
from lawyerAccount.init_speciality import initial_speciality
from ..models import Lawyer, Speciality
from chatting.models import Chatting, Chatting_room
from helpline.models import Report, Log
from helpline.secret.luniverse import *
from helpline.secret.keystore import *
from helpline.secret.keystore import _sha256
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# 비밀번호 변경 시 확인
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
# 이메일 발송
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
# 아이디 중복 체크
from django.http import JsonResponse
# 무작위 패스워드 생성
import string
import random
import hashlib
import json
import time
import datetime
# 에러 메세지 전달
from django.contrib import messages
# 현재 시간
from datetime import datetime

from helpline.secret.aes import AESCipher, make_aes_key
from helpline.unique_key import make_random_key
from core import views, urls
from django.conf.urls.static import static
# 전문분야 초기값 설정
# initial_speciality()


# main page
def home(request):
    return render(request, 'core/main.html')


### 변호사 계정 ###
# 변호사 회원가입
@csrf_exempt
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])

            try:
                lawyer = Lawyer(user=user)
                # 기본사항 입력
                lawyer.name = request.POST.get('name')
                lawyer.image = request.FILES.get('image')
                lawyer.gender = request.POST.get('gender')
                lawyer.phone_number = request.POST.get('phone_number')
                lawyer.email = request.POST.get('email')
                lawyer.find_id_question = request.POST.get('find_id_question')
                lawyer.find_id_answer = request.POST.get('find_id_answer')
                # 주소
                lawyer.home_postcode = request.POST.get('home_postcode')
                lawyer.home_roadAddress = request.POST.get('home_roadAddress')
                lawyer.home_detailAddress = request.POST.get(
                    'home_detailAddress')
                # 학력사항
                lawyer.high_school = request.POST.get('high_school')
                lawyer.high_school_major = request.POST.get(
                    'high_school_major')
                lawyer.high_school_dmission_year = request.POST.get(
                    'high_school_dmission_year')
                lawyer.high_school_graduation_year = request.POST.get(
                    'high_school_graduation_year')
                lawyer.university = request.POST.get('university')
                lawyer.university_major = request.POST.get('university_major')
                lawyer.university_dmission_year = request.POST.get(
                    'university_dmission_year')
                lawyer.university_graduation_year = request.POST.get(
                    'university_graduation_year')
                lawyer.graduate_school = request.POST.get('graduate_school')
                lawyer.graduate_school_major = request.POST.get(
                    'graduate_school_major')
                lawyer.graduate_school_dmission_year = request.POST.get(
                    'graduate_school_dmission_year')
                lawyer.graduate_school_graduation_year = request.POST.get(
                    'graduate_school_graduation_year')
                # 변호사 자격사항
                lawyer.qualification_division = request.POST.get(
                    'qual_category')
                lawyer.qualification_content = request.POST.get('merged_qual')
                lawyer.introduce = request.POST.get('introduce')
                # lawyer.specialty = request.POST.get('merged_specialty')
                lawyer.save()
                user.save()
                speciality_list = [
                    Speciality.objects.get(pk=int(speciality))
                    for speciality in request.POST.getlist('fields', [])
                ]
                lawyer.speciality.add(*speciality_list)
                lawyer.save()

            except Exception as e:
                print(e)
                user.delete()
                return redirect('lawyerAccount:signup')

            auth.login(request, user)
            # messages.error(request, "아직 변호사 권한이 없습니다. 관리자에게 문의하세요.")
            return redirect('lawyerAccount:downloadKS', lawyer.id)

        else:
            # 비밀번호가 다를 시 오류 처리
            return redirect('lawyerAccount:signup')
    else:
        return render(request, 'lawyerAccount/lawyer_form.html', {
            'specialities': Speciality.objects.all(),
        })


def downloadKS(request, user_id):
    if request.method == 'POST':
        return makeKS_lawyer(user_id, request.POST['password'])
    return render(request, "lawyerAccount/downloadKS.html")


# 변호사 로그인

def login(request):
    if request.method == "POST":
        print('post')
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 해당 user가 있으면 username을 없으면 none을 return
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            if user.lawyer.rank == 0:
                messages.error(request, "아직 변호사 권한이 없습니다. 관리자에게 문의하세요.")
                return redirect('lawyerAccount:login')

        else:
            messages.error(request, "입력한 아이디와 비밀번호를 다시 확인해주세요.")
            return redirect('lawyerAccount:login')

        response = redirect('lawyerAccount:checkKS', user.lawyer.id)
        response.set_cookie('who', user.lawyer.id)
        return response

    else:
        response = render(request, "lawyerAccount/login.html")
        response.set_cookie('who', 'login_lawyer')
        return response


# 변호사 로그아웃
def logout(request):
    auth.logout(request)
    response = redirect('core:main')
    response.delete_cookie('who')

    return response


"""
신고서 작성 할 시 set_cookie('who','author')
"""

# 아이디 찾기


def find_id(request):
    find_check = None
    if request.method == "POST":
        question = request.POST.get('find_id_question')
        answer = request.POST.get('find_id_answer')
        context = {}
        try:
            lawyer = Lawyer.objects.get(
                find_id_question=question,
                find_id_answer=answer,
            )
            context['username'] = lawyer.user.username
            find_check = True
        except:
            find_check = False
        context['find_check'] = find_check
        return render(request, 'lawyerAccount/find_id_page.html', context)

    else:
        return render(request, 'lawyerAccount/find_id_page.html')


# 무작위 패스워드 생성
def make_random_password():
    length = 12
    all_letter = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(length):
        password += random.choice(all_letter)
    return password


# 패스워드 찾기
def find_password(request):
    find_check = None
    if request.method == "POST":
        find_check = True
        email = request.POST.get('email')
        context = {'find_check': find_check}
        # try:
        lawyer = Lawyer.objects.get(email=email)
        mail_subject = "[Secret Report] 새로운 비밀번호 입니다."
        new_password = make_random_password()
        # user 비밀번호 변경
        user = lawyer.user
        user.set_password(new_password)
        user.save()

        message = render_to_string(
            'lawyerAccount/change_password_email.html',
            {'new_password': new_password}
        )

        password_email = EmailMessage(
            mail_subject, mark_safe(message), to=[email])
        password_email.send()
        context['message'] = "이메일을 발송하였습니다."
        # except:
        #     context['message'] = "해당 이메일이 존재하지 않습니다."
        return render(request, 'lawyerAccount/find_password_page.html', context)
    else:
        return render(request, 'lawyerAccount/find_password_page.html')


# 비밀번호 변경
def change_password(request, user_id):
    context = {}
    if request.method == "POST":
        origin_password = request.POST.get('origin_password')
        lawyer = Lawyer.objects.get(id=user_id)
        user = lawyer.user
        # 기존 비밀번호 확인
        if check_password(origin_password, user.password):
            new_password = request.POST.get('new_password')
            new_password_check = request.POST.get('new_password_check')
            # 새 비밀번호 확인
            if new_password == new_password_check:
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                return redirect('lawyerAccount:lawyer_edit', lawyer.id)
            else:
                context.update({'error': "새로운 비밀번호를 다시 확인해주세요."})
        else:
            context.update({'error': "현재 비밀번호가 일치하지 않습니다."})

        return render(request, 'lawyerAccount/change_password_page.html', context)

    else:
        return render(request, 'lawyerAccount/change_password_page.html')


# username 중복 검사 (ajax)
def id_overlap_check(request):
    username = request.GET.get('username')

    try:
        # 중복 검사 실패
        user = User.objects.get(username=username)
    except:
        # 중복 검사 성공
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"

    context = {'overlap': overlap}
    return JsonResponse(context)


### 변호사 개인 페이지  ###
# 변호사 개인 페이지
@login_required
def mypage(request, user_id):
    lawyer = None
    try:
        cookie_lawyer_id = int(request.COOKIES.get('who'))
        if cookie_lawyer_id == user_id:
            lawyer = Lawyer.objects.get(id=user_id)
    except:
        return render(request, "lawyerAccount/login.html")

    # 암호화 복호화 과정
    report_list = lawyer.report_set.filter(lawyer_ack='1')

    cnt = 1
    report_list_decrypt = {
        report: {
            'id': report.unique_key,
            'title': report.title,
            'created_at': report.created_at,
        }
        for report in report_list
    }
    report_ack_list = lawyer.report_set.filter(lawyer_ack='2')
    print(report_ack_list, "##########")
    report_ack_list_decrypt = {
        report: {
            'id': report.unique_key,
            'title': report.title,
            'created_at': report.created_at,
        }
        for report in report_ack_list
    }
    print(report_ack_list_decrypt, "!!!!!!!!!!!")

    context = {
        'lawyer': lawyer,
        'report_list_decrypt': report_list_decrypt,
        'report_ack_list_decrypt': report_ack_list_decrypt,
    }
    return render(request, "lawyerAccount/lawyer_my_page.html", context)

# 변호사 정보수정


@login_required
def lawyer_edit(request, user_id):
    lawyer = Lawyer.objects.get(id=user_id)
    if request.method == "POST":
        print("post")
        lawyer.name = request.POST.get('name')
        if request.FILES.get('image') is not None:
            lawyer.image = request.FILES.get('image')
        lawyer.gender = request.POST.get('gender')
        lawyer.phone_number = request.POST.get('phone_number')
        lawyer.email = request.POST.get('email')
        lawyer.find_id_question = request.POST.get('find_id_question')
        lawyer.find_id_answer = request.POST.get('find_id_answer')
        # 주소
        lawyer.home_postcode = request.POST.get('home_postcode')
        lawyer.home_roadAddress = request.POST.get('home_roadAddress')
        lawyer.home_detailAddress = request.POST.get('home_detailAddress')
        # 학력사항
        lawyer.high_school = request.POST.get('high_school')
        lawyer.high_school_major = request.POST.get('high_school_major')
        lawyer.high_school_dmission_year = request.POST.get(
            'high_school_dmission_year')
        lawyer.high_school_graduation_year = request.POST.get(
            'high_school_graduation_year')
        lawyer.university = request.POST.get('university')
        lawyer.university_major = request.POST.get('university_major')
        lawyer.university_dmission_year = request.POST.get(
            'university_dmission_year')
        lawyer.university_graduation_year = request.POST.get(
            'university_graduation_year')
        lawyer.graduate_school = request.POST.get('graduate_school')
        lawyer.graduate_school_major = request.POST.get(
            'graduate_school_major')
        lawyer.graduate_school_dmission_year = request.POST.get(
            'graduate_school_dmission_year')
        lawyer.graduate_school_graduation_year = request.POST.get(
            'graduate_school_graduation_year')
        # 변호사 자격사항
        lawyer.qualification_division = request.POST.get('qual_category')
        if request.POST.get('merged_qual') is not None:
            lawyer.qualification_content = request.POST.get('merged_qual')
        lawyer.introduce = request.POST.get('introduce')
        lawyer.specialty = request.POST.get('merged_specialty')
        print(lawyer)
        lawyer.save()
        print("lawyer.save()")
        return redirect('lawyerAccount:mypage', lawyer.id)

    else:
        context = {
            'lawyer': lawyer,
            'specialities': Speciality.objects.all()
        }
        return render(request, "lawyerAccount/lawyer_edit_page.html", context)

# 변호사한테 온 report


@csrf_exempt
@login_required
def report_page(request, report_id):
    report = Report.objects.get(id=report_id)
    if request.method == 'POST':
        report.lawyer_refuse_msg = request.POST.get('msg')
        report.save()
        return redirect('lawyerAccount:lawyer_refuse', report_id)
    GRASP_CHOICES = (
        ('1', '내게 일어난 일이라서'),
        ('2', '내가 직접 보거나 들은 일이라서'),
        ('3', '직장 동료에게 들었음'),
        ('4', '외부인에게 들었음'),
        ('5', '소문으로 들었음'),
        ('6', '우연히 문서나 파일을 보다가 알게 되었음'),
    )
    TERM_CHOICES = (
        ('1', '한 번'),
        ('2', '일주일'),
        ('3', '1~3개월'),
        ('4', '3개월에서 1년'),
        ('5', '1년 이상'),
    )

    bc_lawyer_id = CreateLawyerId(report.lawyer.id)
    report_hash = hashReport(report)
    inputs = {"_id": CreateRptId(
        report.id), "_user": bc_lawyer_id, "_hashedData": report_hash}
    txId = sendDataToBC('dk9', inputs)
    seed = ''
    key2 = ''
    if txId:
        res = getDataFromBC(txId)

    key1 = AESCipher(report.unique_key)

    if res:
        print(res)
        seed = res['log']['msg']
        log_context = {
            'report': report,
            'timestamp': datetime.fromtimestamp(int(res['log']['_time'])),
            'txHash': res['txHash'],
            'user': res['log']['user']
        }
        log = Log.objects.create(**log_context)
        key2 = key1.decrypt(seed)
        print('lawyer - DESC seed :', key2)

    if not seed:
        key2 = '0.111'
        print('lawyer - default seed : ', key2)

    aes_report = AESCipher(key2)

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
    }
    return render(request, "lawyerAccount/report_page.html", report_context)

# report 승인


def lawyer_ack(request, report_id):
    report = Report.objects.get(id=report_id)
    # 블록체인에 보낼 정보 만들기
    bc_lawyer_id = CreateLawyerId(report.lawyer.id)
    inputs = {"_id": CreateRptId(report.id), "_lawyer": bc_lawyer_id}

    #res = sendDataToBC('al8', inputs)
    report.lawyer_ack = '2'
    report.lawyer_ack_date = datetime.now()
    report.save()
    return redirect('lawyerAccount:mypage', report.lawyer.id)
    # 트랜잭션 성공할 시에 승인으로 변경
    # if res:
    #     report.lawyer_ack = '2'
    #     report.lawyer_ack_date = datetime.now()
    #     report.save()
    #     return redirect('lawyerAccount:mypage', report.lawyer.id)
    # else:
    #     report.lawyer_ack = '2'
    #     report.lawyer_ack_date = datetime.now()
    #     report.save()
    #     return redirect('lawyerAccount:mypage', report.lawyer.id)


# report 거절
def lawyer_refuse(request, report_id):
    report = Report.objects.get(id=report_id)
    redirect_id = report.lawyer.id
    bc_lawyer_id = CreateLawyerId(report.lawyer.id)
    inputs = {"_id": report.unique_key, "_lawyer": bc_lawyer_id}
    res = sendDataToBC('dl9', inputs)
    if res:
        report.lawyer_ack = '3'
        report.lawyer = None
        report.save()
        return redirect('lawyerAccount:mypage', redirect_id)
    else:
        return redirect('lawyerAccount:mypage', redirect_id)

# 변호사 세부 페이지


def lawyer_info(request):
    return render(request, "lawyerAccount/lawyer_info.html")


def checkKS(request, user_id):
    if request.method == 'POST':
        lawyer = Lawyer.objects.get(id=user_id)
        print(lawyer, lawyer.user.username, lawyer.user.password)
        password = request.POST['pw']
        f = request.FILES['keystore']
        keystore = json.loads(f.readline())
        # dict_KS = json.loads(str_KS)
        res = checkKS_lawyer(user_id, password, keystore)
        print(res)
        if res:
            messages.error(request, res)
        else:
            # return redirect('lawyerAccount:mypage', user_id)
            auth.login(request, lawyer.user)
            response = redirect('core:main')
            response.set_cookie('who', lawyer.id)
            return response
    return render(request, "lawyerAccount/checkKS.html")


# def newKS(request):
#     return render(request, "lawyerAccount:downloadKS.html")

@login_required
def reporterInfo(request, report_id):
    report = Report.objects.get(id=report_id)
    reporter = report.author

    bc_lawyer_id = CreateLawyerId(report.lawyer.id)
    author_hash = hashAuthor(reporter)
    inputs = {"_id": CreateRptId(
        report.id), "_user": bc_lawyer_id, "_hashedData": author_hash}
    txId = sendDataToBC('rk9', inputs)

    seed = ''
    key2 = ''
    if txId:
        time.sleep(5)
        res = getDataFromBC(txId)

    key1 = AESCipher(reporter.key)

    if res:
        print(res)
        seed = res['log']['msg']
        # log_context = {
        #     'report': report,
        #     'timestamp': datetime.fromtimestamp(int(res['log']['_time'])),
        #     'txHash': res['txHash'],
        #     'user': res['log']['user']
        # }
        # log = Log.objects.create(**log_context)
        key2 = key1.decrypt(seed)
        print('lawyer - blockchain seed :', key2)

    if not seed:
        key2 = '0.111'
        print('lawyer - default seed : ', key2)

    print(key2)
    key = AESCipher(key2)
    reporter_context = {
        'name': key.decrypt(reporter.name),
        'identification_number': key.decrypt(reporter.identification_number),
        'address': key.decrypt(reporter.address),
        'detail_address': key.decrypt(reporter.detail_address),
        'phone_number': key.decrypt(reporter.phone_number)
    }
    return render(request, "lawyerAccount/reporter_page.html", reporter_context)
