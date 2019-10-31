import requests
import json
import sys

APIkey = sys.argv[1]
networkid = sys.argv[2]
address = sys.argv[3]

url = "https://api.meraki.com/api/v0/networks/"+networkid+"/devices"

headers = {
    'Accept': "*/*",
    'X-Cisco-Meraki-API-Key': APIkey,
    'User-Agent': "PostmanRuntime/7.19.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "cc840ef2-8e18-46c0-a4c5-c4330a225f2d,9a2f97c9-2094-4989-83c0-f07adc99ae11",
    'Accept-Encoding': "gzip, deflate",
    'Referer': "https://api.meraki.com/api/v0/networks/"+networkid+"/devices",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers).text

for json_data in json.loads(response):
    if json_data["address"] == "":
        url = "https://api.meraki.com/api/v0/networks/"+networkid+"/devices/"+json_data["serial"]

        querystring = {"address":address}
        
        payload = "{\r\n  \"serial\": \""+json_data["serial"]+"\"}"
        
        headers = {
            'Accept': "*/*",
            'Content-Type': "application/json",
            'X-Cisco-Meraki-API-Key': APIkey,
            'User-Agent': "PostmanRuntime/7.19.0",
            'Cache-Control': "no-cache",
            'Postman-Token': "65791058-9447-4684-86da-6158024c56ee,3325d8bd-efaf-4a5b-bb32-5eb9e56ed023",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "173",
            'Referer': "https://api.meraki.com/api/v0/networks/"+networkid+"/devices/"+json_data["serial"]+"?address="+address,
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }
        
        response = requests.request("PUT", url, data=payload, headers=headers, params=querystring)