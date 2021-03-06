#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Date: 29/05/2020
# Version: v1

import json
import requests
import socket
import sys
import urllib3
import xmltodict
from datetime import datetime

# Remove warnings
urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connection
ip_pa = sys.argv[1]
port = sys.argv[2]

# URL
key = sys.argv[3]
api = '&cmd=%3Cshow%3E%3Csslmgr-store%3E%3Cconfig-certificate-info%3E%3C%2Fconfig-certificate-info%3E%3C%2Fsslmgr-store%3E%3C%2Fshow%3E'
url = 'https://{}:{}/api/?type=op&cmd=show&key={}{}'.format(ip_pa, port, key, api)

# Telnet 443
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
result_https = sock.connect_ex((ip_pa, int(port)))

# Validate telnet
if result_https != 0:
    sys.exit()

arguments = sys.argv[4]

r = requests.get(url, verify=False)
dados = dict(xmltodict.parse(r.text))
lista = dados['response']['result']
lista = lista.split('\n\n')
result_json = []


# Discovery certified
def discoveryCertified():
    for i in lista:
        result = i.split('\n    ')
        data_fmt = result[6].replace('    db-exp-date: ','')[14:].replace(' GMT)','')
        data = {
            '{#HASH}': result[3].replace('    issuer-subjecthash: ',''),
            '{#ISSUER}': result[2].replace('    issuer: ',''),
            '{#DBEXPDATE}': int(datetime.strptime(data_fmt, '%b %d %H:%M:%S %Y').timestamp()),
            '{#DBSERIAL}': result[8].replace('    db-serialno: ',''),
            '{#DBNAME}': result[10].replace('    db-name: ','')
        }

        result_json.append(data)

    return json.dumps({'data': result_json}, indent=4)


# Date Expirate
def expirationCertified(dbserial):
    lista = discoveryCertified()
    d1_json = json.loads(lista)
    for i in d1_json['data']:
        if dbserial == i['{#DBSERIAL}']:
            expiration = i['{#DBEXPDATE}']
            return expiration


# Script execution with arguments
if arguments == 'discoveryCertified':
    print(discoveryCertificate())
elif arguments == 'expirationCertified':
    cert_serial = sys.argv[5]
    print(expirationCertified(cert_serial))
