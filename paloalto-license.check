#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Date: 15/05/2020
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
api_license_operations = '&cmd=%3Crequest%3E%3Clicense%3E%3Cinfo%3E%3C%2Finfo%3E%3C%2Flicense%3E%3C%2Frequest%3E'
api_license_support = '&cmd=%3Crequest%3E%3Csupport%3E%3Cinfo%3E%3C%2Finfo%3E%3C%2Fsupport%3E%3C%2Frequest%3E'
url_operations = 'https://{}:{}/api/?type=op&cmd=show&key={}{}'.format(ip_pa, port, key, api_license_operations)
url_support = 'https://{}:{}/api/?type=op&cmd=show&key={}{}'.format(ip_pa, port, key, api_license_support)

# Telnet 443
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
result_https = sock.connect_ex((ip_pa, int(port)))

if result_https != 0:
    sys.exit()

arguments = sys.argv[4]

# Discovery Licenses Operations
def discoveryLicensesOperations():
    r = requests.get(url_operations, verify=False)
    dados = dict(xmltodict.parse(r.text))
    lista = dados['response']['result']['licenses']['entry']
    result_json = []

    for i in lista:
        if not i['expires'] == 'Never':
            lista = {
                '{#NAME}': i['feature'],
                '{#SERIAL}': i['serial'],
                '{#ISSUED}': i['issued'],
                '{#EXPIRES}': int(datetime.strptime(i['expires'], '%B %d, %Y').timestamp()),
                '{#EXPIRED}': i['expired']
            }
            result_json.append(lista)

    return json.dumps({'data': result_json}, indent=4)


# Discovery License Support
def discoveryLicenseSupport():
    r = requests.get(url_support, verify=False)
    dados = dict(xmltodict.parse(r.text))
    expirydate = dados['response']['result']['SupportInfoResponse']['Support']['ExpiryDate']
    supportlevel = dados['response']['result']['SupportInfoResponse']['Support']['SupportLevel']
    result_json = []

    lista = {
        '{#NAME}': 'Support',
        '{#EXPIRES}': int(datetime.strptime(expirydate, '%B %d, %Y').timestamp()),
        '{#SUPPORTLEVEL}': supportlevel
    }
    result_json.append(lista)

    return json.dumps({'data': result_json}, indent=4)


# Date expiration licenses operations
def expirationLicensesOperations(license):
    lista = discoveryLicensesOperations()
    d1_json = json.loads(lista)
    for i in d1_json['data']:
        if license == i['{#NAME}']:
            expiration = i['{#EXPIRES}']
            return expiration


# Date expiration licenses support
def expirationLicenseSupport(license):
    lista = discoveryLicenseSupport()
    d1_json = json.loads(lista)
    for i in d1_json['data']:
        if license == i['{#NAME}']:
            expiration = i['{#EXPIRES}']
            return expiration


# Script execution with arguments
if arguments == 'discoveryLicensesOperations':
    print(discoveryLicensesOperations())
elif arguments == 'discoveryLicenseSupport':
    print(discoveryLicenseSupport())
elif arguments == 'expirationLicensesOperations':
    license = sys.argv[5]
    print(expirationLicensesOperations(license))
elif arguments == 'expirationLicenseSupport':
    license = sys.argv[5]
    print(expirationLicenseSupport(license))
