from lawyerAccount.models import Speciality


def initial_speciality():
    speciality_list = [
        '형사',
        '민사',
        '가정',
        '성범죄',
        '인권',
        '노동',
        '비리',
        '행정',
        '금융',
        '의료',
        '건설',
        '기업',
        '공정거래',
        '상법',
        '인터넷'
    ]
    for speciality in speciality_list:
        Speciality.objects.create(name=speciality)
