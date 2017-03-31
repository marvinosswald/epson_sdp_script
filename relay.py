#!/usr/bin/python
import requests
import os

printerId = os.environ['PRINTER_ID']
printerIp = os.environ['PRINTER_IP']
server = os.environ['SERVER_URL']
printerToken = os.environ['SERVER_AUTH_TOKEN']
xmlNoDeviceFound = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ><soapenv:Body><response success="false" code="DeviceNotFound" status="251854908" battery="0" xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print"/></soapenv:Body></soapenv:Envelope>'


response = requests.post(server + '/api/printers/'+printerId+'/jobs',headers={'Authorization':'Bearer ' + printerToken},params={'ConnectionType':'GetRequest'})
if response.status_code == requests.codes.ok:
    try:
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
                          data=xmlNoDeviceFound)
    except:
        requests.post(server +'/api/printers/' + printerId + '/jobs',
                      headers={'Authorization': 'Bearer ' + printerToken},
                      params={'ConnectionType': 'SetRequest'},
                      data=xmlNoDeviceFound)