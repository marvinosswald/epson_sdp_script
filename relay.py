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


response = requests.post(server + '/api/printers/'+printerId+'/jobs',headers={'Authorization':'Bearer ' + printerToken},params={'ConnectionType':'GetRequest'})
if response.status_code == requests.codes.ok:
    try:
        printerResponse = requests.post('http://'+printerIp + '/cgi-bin/epos/service.cgi?devid='+printerId+'&timeout=10000',data=response.text)
        if printerResponse.status_code == requests.codes.ok:
            xmlNoDeviceFound = printerResponse
            response = requests.post(server +'/api/printers/' + printerId + '/jobs',
                                 headers={'Authorization': 'Bearer ' + printerToken},
                                 data=printerResponse,
                                 params={'ConnectionType':'SetRequest'})
        else:
            requests.post(server +'/api/printers/' + printerId + '/jobs',
                          headers={'Authorization': 'Bearer ' + printerToken},
                          params={'ConnectionType': 'SetRequest'},
                          data=printerResponse)
    except:
        requests.post(server +'/api/printers/' + printerId + '/jobs',
                      headers={'Authorization': 'Bearer ' + printerToken},
                      params={'ConnectionType': 'SetRequest'},
                      data=xmlNoDeviceFound)