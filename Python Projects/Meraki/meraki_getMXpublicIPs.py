import requests
import json
import sys


# this is your API key dont' use mine
APIkey = sys.argv[1]

# the first request gives us a list of organizations that are associated with your API key
url = "https://api.meraki.com/api/v0/organizations"

payload = {}
headers = {
  'X-Cisco-Meraki-API-Key': APIkey,
  'baseUrl': 'https://api.meraki.com/api/v0'
}

response = requests.request("GET", url, headers=headers, data = payload).text

org_data = []

# we want to make our own object that contains the response from the API
# this is because we want to add a menu identifier to each organization
menu_count = 1
for one_org_data in json.loads(response):
    one_org_data["menu"] = menu_count
    menu_count += 1
    org_data.append(one_org_data.copy())

# then we build a nice little menu so you can selection the organization you want
choice = 0
while choice == 0:
    print ("Organizations:")
    for data in org_data:
        print(data["menu"],data["name"])
     
    choice = int(input ("Please choose an organization: "))
     
    for data in org_data:
        if choice == data["menu"]:
            print("You selected the organization",data["name"])
            organization = data["id"]

# then we build a nice little menu so you can selection the organization you want
readable = 11
while readable == 11:
    print ("Now you get to choose the output format!")
    print("1: Human readble")
    print("2: CSV")
     
    readable = int(input ("Please choose your output format: "))
     
    if readable == 1:
        print("Human readable it is!")
    else:
        print("Okay you're getting CSV")
        readable = 0
    print()

# now that we know what organization you want, we comb through the inventory looking for firewalls
url = "https://api.meraki.com/api/v0/organizations/"+organization+"/inventory"
response = requests.request("GET", url, headers=headers, data = payload).text

org_mx = []

# we make a little list of dictionaries to contain the MX appliance data
for org_devices in json.loads(response):
    if "MX" in org_devices["model"]:
        org_mx.append(org_devices.copy())



# then we iterate through this list, and pull down the uplink info for each MX device
for mx_list in org_mx:
    line = []
    url = "https://api.meraki.com/api/v0/networks/"+mx_list["networkId"]+"/devices/"+mx_list["serial"]+"/uplink"
    response = requests.request("GET", url, headers=headers, data = payload).text
    
    if readable:
        print(mx_list["name"])
    else:
        line.append(mx_list["name"])
    
    # each MX has two uplinks so we iterate through them
    for mx_uplinks in json.loads(response):
        # the other variables don't exist if the link is down, and it makes the script barf
        # I could have coded error handling for that, but it is easier to just avoid it
        if mx_uplinks["status"] == "Not connected":
            if readable:
                try:
                    print(mx_uplinks["interface"],"Not connected")
                except KeyError:
                    pass
            else:
                try:
                    line.append(mx_uplinks["interface"])
                except KeyError:
                    line.append("")
                line.append("Not connected")
        else:
            if readable:
                try:
                    print(mx_uplinks["interface"],end='')
                except KeyError:
                    pass
                try:
                    print(mx_uplinks["status"],end='')
                except KeyError:
                    pass
                print()
            else:
                try:
                    line.append(mx_uplinks["interface"])
                except KeyError:
                    line.append("")
                try:
                    line.append(mx_uplinks["status"])
                except KeyError:
                    line.append("")
            if readable:
                try:
                    print("IP Address",mx_uplinks["ip"],end='')
                except KeyError:
                    pass
                try:
                    print("Gateway IP",mx_uplinks["gateway"],end='')
                except KeyError:
                    pass
                try:
                    print("DNS",mx_uplinks["dns"],end='')
                except KeyError:
                    pass
                print()
            else:
                line.append("IP Address")
                try:
                    line.append(mx_uplinks["ip"])
                except KeyError:
                    line.append("")
                line.append("Gateway IP")
                try:
                    line.append(mx_uplinks["gateway"])
                except KeyError:
                    line.append("")
                line.append("DNS")
                try:
                    line.append(mx_uplinks["dns"])
                except KeyError:
                    line.append("")
            if mx_uplinks["usingStaticIp"]:
                if readable:
                    print("Using Static IP")
                else:
                    line.append("Using Static IP")
            else:
                if readable:
                    print("Using Dynamic IP")
                else:
                    line.append("Using Dynamic IP")
    if readable:
        print()
    else:
        print(",".join(line))