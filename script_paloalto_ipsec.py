#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Date: 13/05/2020
# Version: v1

import json
import re
import requests
import socket
import sys
import urllib3
import xmltodict

# Remove warnings
urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connection
ip_pa = sys.argv[1]
port = sys.argv[2]

# URL
key = sys.argv[3]
api_vpn = '&cmd=%3Cshow%3E%3Cvpn%3E%3Cflow%3E%3C%2Fflow%3E%3C%2Fvpn%3E%3C%2Fshow%3E'
url = f'https://{ip_pa}:{port}/api/?type=op&cmd=show&key={key}{api_vpn}'

# Telnet 443
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
result_https = sock.connect_ex((ip_pa, int(port)))

if result_https != 0:
    sys.exit()

arguments = sys.argv[4]


# Discovery VPN
def discovery_vpn():
    r = requests.get(url, verify=False)
    dados = dict(xmltodict.parse(r.text))
    lista = dados['response']['result']['IPSec']['entry']
    result_json = []

    for i in lista:
        lista = {
            '{#NAME}': i['name'],
            '{#PEERIP}': i['peerip'],
            '{#TUNNEL}': i['inner-if'],
            '{#STATUS}': i['state'],
            '{#MON}': i['mon']
        }
        result_json.append(lista)

    return json.dumps({'data': result_json}, indent=4)


# State VPN
def status_vpn(vpn_name):
    lista = discovery_vpn()
    d1_json = json.loads(lista)

    for i in d1_json['data']:

        if vpn_name == i['{#NAME}']:
            status = i['{#STATUS}']

            if 'active' == status:
                return 1
            elif 'inactive' == status:
                return 0
            else:
                return 2


# Script execution with arguments
if arguments == 'discovery_vpn':
    print(discovery_vpn())

elif arguments == 'status_vpn':
    vpn_name = sys.argv[5]
    print(status_vpn(vpn_name))
