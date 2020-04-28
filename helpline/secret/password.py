import hashlib


# 인자로 들어온 password 를 암호화하여 반환하는 함수
def generate_password(password):
    hash_pw = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hash_pw


# 사용자가 입력한 비밀번호가 맞는지 확인하는 함수
def check_password(password, input_password):
    if password == generate_password(input_password):
        return True
    return False
