import requests

import sys
import time

# this is your API key
APIkey = sys.argv[1]

# use an API tool to learn the network ID
# I used postman
networkid = sys.argv[2]

# filename with the VLAN list you want to modify
VLANfile = sys.argv[3]

# the DSCP marking we want to use
DSCP = sys.argv[4]

# first we create the API request URL
# this will let us learn ALL the devices that are part of this particular network
# and then we can iterate through them and set the physical shipping address
url = "https://api.meraki.com/api/v0/networks/"+networkid+"/switch/settings/qosRules"

# then we set the header
# we carefully insert the correct API key, yours not mine
headers = {
  'X-Cisco-Meraki-API-Key': APIkey,
  'baseUrl': 'https://api.meraki.com/api/v0',
  'Accept': '*/*',
  'Content-Type': 'application/json'
}

# we open the VLAN list file
VLANlist = open(VLANfile,'r')

# now we iterate through the list of devices in this network
for VLAN in VLANlist:
    
    # we only set the physical shipping address for devices that don't already have an adddress set
    # I figure if someone has taken the time to set this, they probably know what they're doing
    # that said you could remove this if statement and just overwrite what is there
    payload = "{\n  \"vlan\": "+VLAN+",\n  \"protocol\": \"Any\",\n  \"dscp\": "+DSCP+"\n}"
    
    print(url)
    print(headers)
    print(payload)
    response = requests.request("POST", url, headers=headers, data = payload)
    
    print(response.text.encode('utf8'))
    
    # we sloooooooow down because Meraki has a hard limit of 5 API calls per second
    # I didn't hit the limit with this script, but the result is a 404 and rather than
    # try to code in error handling for that, I figure we can just stay under the limit
    # I'm lazy it is true.
    time.sleep(0.2)