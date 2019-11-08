#import requests
import json
import sys
#import time

APIkey = sys.argv[1]
serial = sys.argv[2]
config = sys.argv[3]
switchport = 0

url = "https://api.meraki.com/api/v0/devices/"+serial+"/switchPorts/"+str(switchport)

headers = {
    'Accept': "*/*",
    'Content-Type': "application/json",
    'X-Cisco-Meraki-API-Key': APIkey,
    'User-Agent': "PostmanRuntime/7.19.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "31cf524b-dbee-4751-80fe-c22f4b3e1513,67911d68-586e-4b01-af59-ecab387a84f7",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "301",
    'Referer': "https://api.meraki.com/api/v0/devices/"+serial+"/switchPorts/"+str(switchport),
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

with open(config) as f:
    config_json = json.load(f)
    print(config_json)