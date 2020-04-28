import random
import string


# length 만큼의 영어 대소문자와 숫자를 결합한 문자열을 만들어 반환하는 함수
def make_random_key():
    length = 8
    string_pool = string.ascii_letters + string.digits

    result = ""
    for i in range(length):
        result += random.choice(string_pool)
    return result


# Report 의 신고서 ID 는 유일해야하기 때문에 해당값이 유일할 때 반환하는 함수
def make_unique_key():
    from helpline.models import Report
    unique_number_list = [number[0]
                          for number in Report.objects.values_list('unique_key')]
    random_key = make_random_key()
    while random_key in unique_number_list:
        random_key = make_random_key()
    return random_key


def make_random_key_16():
    length = 16
    string_pool = string.ascii_letters + string.digits

    result = ""
    for i in range(length):
        result += random.choice(string_pool)
    return result
