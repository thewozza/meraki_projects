import requests
import json
import sys
import time

APIkey = sys.argv[1]
serial = sys.argv[2]
config = sys.argv[3]

with open(config) as f:
    config_json = json.load(f)

switchport_list = 0

while switchport_list < len(config_json):
    switchport = switchport_list + 1
    time.sleep(0.2)
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

    print(config_json[switchport_list])
    
    for key in config_json[switchport_list].copy():
        if not isinstance(config_json[switchport_list][key], (int, float)):
            if not config_json[switchport_list][key]:
                config_json[switchport_list].pop(key)
                continue
    
    payload = json.dumps(config_json[switchport_list])
 
    print(payload)
    
    response = requests.request("PUT", url, data=payload, headers=headers)
      
    print(response.text)

    switchport_list += 1
