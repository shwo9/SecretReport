from helpline.models import Report
from lawyerAccount.models import Lawyer
from helpline.unique_key import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
import io
import json
import requests
import hashlib
import string


def makeKS_lawyer(lawyer_id, password):
    lawyer = Lawyer.objects.get(id=lawyer_id)

    # 변호사 키스토어 버젼 이용해서  idSeed 만들기
    verNum = (int(lawyer.keyVersion[0])+1) % 10
    ver = str(verNum) + make_random_key()

    # update keyversion for keystore downloaded recently
    lawyer.keyVersion = ver
    lawyer.save()

    # salt seed 랜덤생성
    saltSeed = make_random_key_16()

    # id, salt, mac 생성
    keystore_id = CreateLawyerId(lawyer_id)
    version = _sha256(lawyer.keyVersion)
    salt = _sha256(saltSeed)
    mac = _sha256(salt+password)

    keystore = {"id": keystore_id,
                "version": version, "salt": salt, "mac": mac}
    text = json.dumps(keystore)
    response = HttpResponse(text, content_type='txt/plain')
    response['Content-Disposition'] = 'attachment; filename = keystore'
    return response


def checkKS_lawyer(lawyer_id, password, ks):
    lawyer = Lawyer.objects.get(id=lawyer_id)
    _id = CreateLawyerId(lawyer_id)
    _version = _sha256(lawyer.keyVersion)
    _mac = _sha256(ks['salt'] + password)

    if ks['id'] != _id or ks['version'] != _version:
        return '잘못된 키스토어입니다.'
    elif ks['mac'] != _mac:
        return '비밀번호를 다시 확인해주세요'
    else:
        return False


def _sha256(input):
    return str(hashlib.sha256(input.encode()).hexdigest())


def CreateLawyerId(lawyer_id):
    lawyer = Lawyer.objects.get(id=lawyer_id)
    return _sha256(lawyer.user.username + lawyer.user.password)


def CreateRptId(report_id):
    report = Report.objects.get(id=report_id)
    return _sha256(report.unique_key)


def CreateRpterId(report_id):
    report = Report.objects.get(id=report_id)
    return _sha256(report.unique_key + report.password)
