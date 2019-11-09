import requests
import json
import sys
import time

# this is your API key
APIkey = sys.argv[1]

# use an API tool to learn the organization ID
# I used postman
orgid = sys.argv[2]

# use an API tool to learn the network ID
# I used postman
networkid = sys.argv[3]

# first we create the API request URL
# this will let us learn the alerts configuration for this particular network
# then we can copy this to all the other networks in this organization
url = "https://api.meraki.com/api/v0/networks/"+networkid+"/alertSettings"

# then we set the header
# we carefully insert the correct API key, yours not mine
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

# the results of this first API request get put into a json data structure
# in this case it looks very much like a list of dicts
# the .text at the end makes it a string result, instead of a weird byte structure
# that I don't know how to deal with
alerts_main = requests.request("GET", url, headers=headers).text

# next we create another API request URL
# this will let us learn the networks for this organization
# we'll be able to iterate through this list and push the alerts configuration we just learned to each of them
url = "https://api.meraki.com/api/v0/organizations/"+orgid+"/networks"

# then we set the header
# we carefully insert the correct API key, yours not mine
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

# now we've got a json data structure that contains all the networks we need to look at
networks = requests.request("GET", url, headers=headers).text

# let's get to work
# we iterate through that list of networks
for network_json in json.loads(networks):

    # I left this debugging piece in, because it is nice to know what network your script
    # is diddling when you're running something that can wreak havok across your entire 
    # organization
    print(network_json["name"])
    
    # we sloooooooow down because Meraki has a hard limit of 5 API calls per second
    # I didn't hit the limit with this script, but the result is a 404 and rather than
    # try to code in error handling for that, I figure we can just stay under the limit
    # I'm lazy it is true.
    time.sleep(0.2)
   
    # next we create another API request URL
    # this will let us push the alert settings to this particular network
    # the id key references the unique network number for this network
    url = "https://api.meraki.com/api/v0/networks/"+network_json["id"]+"/alertSettings"
    
    # then we set the header
    # we carefully insert the correct API key, yours not mine
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
    
    # finally this is what we came for.
    # we PUT the alerts payload and the headers
    # this effectively copies the alerts from our supplied example network to all the other networks in this organization 
    response = requests.request("PUT", url, data=alerts_main, headers=headers)

    # you don't need this step, but here the API will send back the current configuration 
    # of whatever API element you were tickling.
    # in this case it is the alerts settings for this network, and this should match what is in the PUT
    # which you can verify with a print(alerts_main)
    print(response.text)