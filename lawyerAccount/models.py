from django.db import models

from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    image = ProcessedImageField(blank=True, null=True,
                                processors=[Thumbnail(400, 400)],
                                format='JPEG',
                                options={'quality': 60})
    gender = models.CharField(
        choices=[("man", "남성"), ("woman", "여성")], max_length=10)
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField()

    find_id_question = models.CharField(max_length=50)
    find_id_answer = models.CharField(max_length=20)

    # 사무실 주소
    home_postcode = models.CharField(max_length=10)
    home_roadAddress = models.CharField(max_length=100)
    home_detailAddress = models.CharField(max_length=100)

    # 학력사항
    high_school = models.CharField(max_length=20)
    high_school_major = models.CharField(max_length=10)
    high_school_dmission_year = models.CharField(max_length=15, blank=True)
    high_school_graduation_year = models.CharField(max_length=15, blank=True)
    university = models.CharField(max_length=20)
    university_major = models.CharField(max_length=10)
    university_dmission_year = models.CharField(max_length=15, blank=True)
    university_graduation_year = models.CharField(max_length=15, blank=True)
    graduate_school = models.CharField(max_length=20)
    graduate_school_major = models.CharField(max_length=10)
    graduate_school_dmission_year = models.CharField(max_length=15, blank=True)
    graduate_school_graduation_year = models.CharField(
        max_length=15, blank=True)

    # 변호사 자격사항
    qualification_division = models.CharField(max_length=5, choices=[(
        "1", "사법연수원 수료자-공직 경력 없음"), ("2", "변호사 시험 합격자-공직 경력없음"), ("3", "판,검사"), ("4", "판,검사외 전 ,현직 모든 공직경력자 [재판 연구원, 경찰, 단기군법무관(법무관 병역 복무),공무원등]"), ("5", "군법무관")])
    qualification_content = models.CharField(max_length=50, default="")
    # qualification_test_num = models.PositiveSmallIntegerField()
    # qualification_date = models.DateField()
    # qualification_th = models.PositiveSmallIntegerField()
    # qualification_completion_date = models.DateField()
    # # choices 각 학교들은 나중에 채워주자.
    # law_school = models.CharField(max_length=10, choices=[("KNU","강원대학교"),("KU","건국대학교")])
    # 자기소개
    introduce = models.TextField()
    # 전문분야
    speciality = models.ManyToManyField('Speciality')

    # rank 가 0이면 아직 미인증, 1은 일반변호사, 2는 신뢰가는 변호사
    rank = models.IntegerField(default=0, choices=[(
        0, "인증 대기 상태"), (1, "일반 변호사"), (2, "신뢰가는 변호사")])

    # 변호사 평가 점수
    rating = models.FloatField(default=0)

    # keystore version
    keyVersion = models.CharField(max_length=9, default='000000000')

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
