#!/usr/bin/python
import requests
import ConfigParser, os

config = ConfigParser.ConfigParser()
config.read('./config.cfg')

printerId = config.get('PRINTER','ID')
printerIp = config.get('PRINTER','IP')
server = config.get('SERVER','URL')
printerToken = config.get('SERVER','AUTH_TOKEN')
xmlNoDeviceFound = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ><soapenv:Body><response success="false" code="DeviceNotFound" status="251854908" battery="0" xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print"/></soapenv:Body></soapenv:Envelope>'
pingXML= '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ><s:Header><parameter xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print"><devid>local_printer</devid><printjobid>AAA</printjobid></parameter></s:Header><soapenv:Body></soapenv:Body></soapenv:Envelope>'

try:
    ping = requests.post('http://'+printerIp + '/cgi-bin/epos/service.cgi?devid='+printerId+'&timeout=10000',data=pingXML)
except:
    requests.post(server + '/api/printers/' + printerId + '/jobs',
                  headers={'Authorization': 'Bearer ' + printerToken},
                  params={'ConnectionType': 'SetRequest'},
                  data=xmlNoDeviceFound)

if 'ping' in locals() and ping.status_code == requests.codes.ok:
    response = requests.post(server + '/api/printers/'+printerId+'/jobs',headers={'Authorization':'Bearer ' + printerToken},params={'ConnectionType':'GetRequest'})
    if response.status_code == requests.codes.ok:
            printerResponse = requests.post('http://'+printerIp + '/cgi-bin/epos/service.cgi?devid='+printerId+'&timeout=10000',data=response.text)
            if printerResponse.status_code == requests.codes.ok:
                response = requests.post(server +'/api/printers/' + printerId + '/jobs',
                                     headers={'Authorization': 'Bearer ' + printerToken},
                                     data=printerResponse,
                                     params={'ConnectionType':'SetRequest'})
            else:
                requests.post(server +'/api/printers/' + printerId + '/jobs',
                              headers={'Authorization': 'Bearer ' + printerToken},
                              params={'ConnectionType': 'SetRequest'},
                              data=printerResponse)