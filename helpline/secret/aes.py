# -*- coding:utf-8 -*-


import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

import random
import string


# 암호화, 복호화를 위한 클래스(encrypt, decrypt method 가 각각 암호화, 복호화에 사용된다)
class AESCipher:
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


# Report 의 Author 의 정보를 암호화, 복호화할 때 사용되는 key 값(16자리)을 반환하는 함수
def make_aes_key():
    length = 16
    string_pool = string.ascii_letters + string.digits

    result = ""
    for i in range(length):
        result += random.choice(string_pool)
    return result
