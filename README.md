# PaloAlto Zabbix Scripts

Zabbix scripts to monitor additional PaloAlto metrics.

## Installation

- Install the scripts in your Zabbix externalscripts folder.
- Install the appropriate dependencies:
  - requests
  - urllib3
  - xmltodict
- Generate an API token for your devices:
  - *NOTE* It is recommended to use a read-only user for monitoring 
  - `curl -k -X POST https://<firewall>/api/?type=keygen&user=<username>&password=<password>`
- Import the template-paloalto-extra.xml in to Zabbix, and apply the `Template Palo Alto Extra` template.

