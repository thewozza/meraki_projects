import requests
import json
import sys
import time

APIkey = sys.argv[1]
orgid = sys.argv[2]
networkid = sys.argv[3]


url = "https://api.meraki.com/api/v0/networks/"+networkid+"/alertSettings"

headers = {
    'Accept': "*/*",
    'X-Cisco-Meraki-API-Key': APIkey,
    'User-Agent': "PostmanRuntime/7.19.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "cc840ef2-8e18-46c0-a4c5-c4330a225f2d,9a2f97c9-2094-4989-83c0-f07adc99ae11",
    'Accept-Encoding': "gzip, deflate",
    'Referer': "https://api.meraki.com/api/v0/networks/"+networkid+"/alertSettings",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

alerts_main = requests.request("GET", url, headers=headers).text

url = "https://api.meraki.com/api/v0/organizations/"+orgid+"/networks"

headers = {
    'Accept': "*/*",
    'X-Cisco-Meraki-API-Key': APIkey,
    'User-Agent': "PostmanRuntime/7.19.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "c00bc44b-e02f-47ed-bbc7-d8e960ccdc3f,6d8582c7-c8d0-400e-976f-d23ca62c884e",
    'Accept-Encoding': "gzip, deflate",
    'Referer': "https://api.meraki.com/api/v0/organizations/"+orgid+"/networks",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

networks = requests.request("GET", url, headers=headers).text

for network_json in json.loads(networks):

    print(network_json["name"])
    
    time.sleep(0.2)
   
    url = "https://api.meraki.com/api/v0/networks/"+network_json["id"]+"/alertSettings"

    headers = {
        'Accept': "*/*",
        'Content-Type': "application/json",
        'X-Cisco-Meraki-API-Key': APIkey,
        'User-Agent': "PostmanRuntime/7.19.0",
        'Cache-Control': "no-cache",
        'Postman-Token': "242faef5-ba9d-4281-88e7-492a724a371b,e9a0fc3a-2eb2-43d1-b5ea-a4835664268b",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "95",
        'Referer': "https://api.meraki.com/api/v0/networks/"+network_json["id"]+"/alertSettings",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    
    response = requests.request("PUT", url, data=alerts_main, headers=headers)

    print(response.text)