from helpline.models import Report
from helpline.secret.keystore import _sha256
import io
import json
import time
import requests
import hashlib
import string


def makeReporterKey():
    pass


def makeLawyerKey():
    pass


def sendDataToBC(action, inputs):
    URL = 'https://api.luniverse.io/tx/v1.0/transactions/' + action
    params = {"from": "0x3f9b648698e43f1cac6d6fa56852edccd7d96e99",
              "inputs": inputs}
    _data = json.dumps(params)
    response = requests.post(URL, headers={"Authorization": "Bearer EgyURTQvbktzd8miKcPdvco4YaAiev6fYZDU6UTEty6ZVUMfgp9jKYg5oyAd7fkQ",
                                           "Content-Type": "application/json"}, data=_data)

    result = json.loads(response.text)
    print(result)

    if 'txId' in result['data']:
        return result['data']['txId']
    return False


def getDataFromBC(action):
    URL = 'https://api.luniverse.io/tx/v1.0/histories/' + action
    time.sleep(1.8)
    response = requests.get(URL, headers={"Authorization": "Bearer EgyURTQvbktzd8miKcPdvco4YaAiev6fYZDU6UTEty6ZVUMfgp9jKYg5oyAd7fkQ",
                                          "Content-Type": "application/json"},)
    result = json.loads(response.text)
    i = 1.8
    while result['data']['history']['txStatus'] != 'SUCCEED':
        time.sleep(0.2)
        i += 0.2

        response = requests.get(URL, headers={"Authorization": "Bearer EgyURTQvbktzd8miKcPdvco4YaAiev6fYZDU6UTEty6ZVUMfgp9jKYg5oyAd7fkQ",
                                              "Content-Type": "application/json"},)
        result = json.loads(response.text)
    print("걸린 시간:", round(i, 2))
    print(result)
    print('succeed.....')
    return {'log': result['data']['history']['txReceipt']['logs'][0]['inputs'], 'txHash': result['data']['history']['txHash']}


def hashReport(report):
    temp = ''
    temp = str(report.organization) + str(report.title) + str(report.who) + str(report.when) + str(report.where) + \
        str(report.content)+str(report.witness) + \
        str(report.method) + str(report.grasp) + str(report.term)

    return _sha256(temp)


def hashAuthor(author):
    temp = ''
    temp = str(author.name) + str(author.identification_number) + str(author.address) + \
        str(author.detail_address) + str(author.phone_number) + str(author.key)

    return _sha256(temp)
