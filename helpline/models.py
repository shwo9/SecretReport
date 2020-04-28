# -*- coding: utf-8 -*-
import os
import uuid

from django.db import models
from django.urls import reverse

from lawyerAccount.models import Lawyer


# 신고 기관 모델
class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name='기관명')

    def __str__(self):
        return self.name


# 신고자 모델
class Author(models.Model):
    # TODO: + 암호화(복호화 가능하게)
    name = models.CharField(max_length=108, verbose_name='이름')
    identification_number = models.CharField(
        max_length=64, verbose_name='주민등록번호')
    address = models.CharField(max_length=216, verbose_name='주소')
    detail_address = models.CharField(max_length=216, verbose_name='거주지')
    phone_number = models.CharField(max_length=64, verbose_name='연락처')
    key = models.CharField(max_length=16, blank=True)


# 신고서 모델
# 해당 모델은 신고자 모델(Author), 신고 기관 모델(Organization),
#           변호사 모델(lawyer), 신고서 첨부파일 모델(ReportFile) 과 연결되어 있음.
class Report(models.Model):
    LAWYER_ACK_CHOICES = (
        ('1', '승인 대기 중'),
        ('2', '승인'),
        ('3', '거절')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_key = models.CharField(max_length=8, unique=True)
    author = models.OneToOneField(
        Author, on_delete=models.CASCADE, verbose_name='신고자')
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name='기관명')
    title = models.TextField(verbose_name='제목')
    who = models.TextField(verbose_name='누가')
    when = models.TextField(verbose_name='언제')
    where = models.TextField(verbose_name='어디서')
    content = models.TextField(verbose_name='내용')
    witness = models.TextField(verbose_name='문제를 아는 사람')
    method = models.TextField(verbose_name='문제 확인 방법')
    grasp = models.CharField(max_length=108, verbose_name='파악 경위')
    term = models.CharField(max_length=64, verbose_name='기간')
    password = models.CharField(max_length=32, verbose_name='비밀번호')
    created_at = models.DateTimeField(auto_now_add=True)

    lawyer = models.ForeignKey(
        Lawyer, on_delete=models.CASCADE, blank=True, null=True, verbose_name='변호사')
    lawyer_ack_date = models.DateField(null=True, blank=True)
    lawyer_ack = models.CharField(
        max_length=1, choices=LAWYER_ACK_CHOICES, default='1', verbose_name='수임 여부')
    lawyer_refuse_msg = models.TextField(
        null=True, blank=True, verbose_name='거절 사유')

    def get_absolute_url(self):
        return reverse('helpline:report_detail', args=[self.id])


# 신고서 첨부파일 모델
class ReportFile(models.Model):
    file = models.FileField(
        upload_to="helpline/report/%Y/%m/%d", verbose_name='첨부파일')
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, verbose_name="신고서")

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.filename()


class Log(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, verbose_name="신고서")
    timestamp = models.DateTimeField(verbose_name='시간')
    txHash = models.CharField(max_length=64, verbose_name="TxHash")
    user = models.CharField(max_length=10, verbose_name="user")
