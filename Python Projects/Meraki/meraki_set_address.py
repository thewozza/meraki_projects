import requests
import json
import sys
import time

# this is your API key
APIkey = sys.argv[1]

# use an API tool to learn the network ID
# I used postman
networkid = sys.argv[2]

# this is the physical shipping address that you want to set
address = sys.argv[3]

# first we create the API request URL
# this will let us learn ALL the devices that are part of this particular network
# and then we can iterate through them and set the physical shipping address
url = "https://api.meraki.com/api/v0/networks/"+networkid+"/devices"

# then we set the header
# we carefully insert the correct API key, yours not mine
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

# the results of this first API request get put into a json data structure
# in this case it looks very much like a list of dicts
# the .text at the end makes it a string result, instead of a weird byte structure
# that I don't know how to deal with
response = requests.request("GET", url, headers=headers).text

# now we iterate through the list of devices in this network
for json_data in json.loads(response):
    
    # we only set the physical shipping address for devices that don't already have an adddress set
    # I figure if someone has taken the time to set this, they probably know what they're doing
    # that said you could remove this if statement and just overwrite what is there
    if json_data["address"] == "":
        
        # we sloooooooow down because Meraki has a hard limit of 5 API calls per second
        # I didn't hit the limit with this script, but the result is a 404 and rather than
        # try to code in error handling for that, I figure we can just stay under the limit
        # I'm lazy it is true.
        time.sleep(0.2)
        
        # this URL references the network and the individual device that we're setting the
        # physical shipping address for
        url = "https://api.meraki.com/api/v0/networks/"+networkid+"/devices/"+json_data["serial"]
        
        # I'm not entirely sure why this isn't part of the payload
        # all the other PUT API that I've seen with Meraki just use the payload
        # but we don't ask questions, this is what it is
        querystring = {"address":address}
        
        # the structure of the payload is really simple
        # the \r\n stuff and the spaces are NOT significant, they just make it nicer to view
        # when you're debugging, you can just print (payload) and it looks pretty
        payload = "{\r\n  \"serial\": \""+json_data["serial"]+"\"}"
        
        # then we set the header
        # we carefully insert the correct API key, yours not mine
        # I'm not entirely sure how important the header data is but since it seems to reference
        # all the components involved, I'm going to guess that it is important
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
        
        # finally this is what we came for.
        # we PUT the payload, headers and the weird querystring param and this updates the
        # physical shipping address
        response = requests.request("PUT", url, data=payload, headers=headers, params=querystring)