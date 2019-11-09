import requests
import json
import sys
import time

# this is your API key
APIkey = sys.argv[1]

# this is the serial number of the switch that you're pushing the config to
serial = sys.argv[2]

# this is the json file of the configuration you're pushing
# I created this on my system using postman and the getDeviceSwitchPorts API
# https://api.meraki.com/api/v0/devices/:serial/switchPorts
# this outputs a json blob with the configuration for each switch port
# then I saved it to a file and we can use it here
config = sys.argv[3]

# we open that config file, and hopefully it is a json file because I don't have any error
# handling here
with open(config) as f:
    config_json = json.load(f)

# okay this is going to be a little confusing at first but....
# in python lists are itemized as 0...9
# but Meraki switchports are itemized as 1..10
# so this means that list element 0 is actually switchport 1
# and list element 9 is actually switchport 10
# so we'll deal with this by just adding one when we need to
switchport_list = 0
# but first we initialize the list element

# we want to iterate over the config file one interface at a time
# it is essentially a list of dicts so we'll go one list element at a time
# which gives us one dict object to work with
while switchport_list < len(config_json):
    
    # remember how I said we'd have to add one?
    switchport = switchport_list + 1
    
    # we sloooooooow down because Meraki has a hard limit of 5 API calls per second
    # I didn't hit the limit with this script, but the result is a 404 and rather than
    # try to code in error handling for that, I figure we can just stay under the limit
    # I'm lazy it is true.
    time.sleep(0.2)
    
    # first we create the API request URL
    # this will let us push the configuration for THIS ONE INTERFACE
    # seriously yes we have to do this one interface at a time
    url = "https://api.meraki.com/api/v0/devices/"+serial+"/switchPorts/"+str(switchport)

    # then we set the header
    # we carefully insert the correct API key, yours not mine
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

    # I guess this is just debugging stuff
    # but it shows the configuration we're intending to push
    # which is always nice to see before the script blows up your network
    print(config_json[switchport_list])
    
    # this little beauty deletes any null elements in the config
    # Meraki will happily give you the null values, but they sure as shit don't
    # want you submitting empty values back to them.
    for key in config_json[switchport_list].copy():
        if not isinstance(config_json[switchport_list][key], (int, float)):
            if not config_json[switchport_list][key]:
                config_json[switchport_list].pop(key)
                continue
    
    # now we can dump that dictionary back into real json for the payload
    # believe it or not I did this painstakingly by hand until I realized there's a 
    # json function for it.  it is pretty nice that it is there.
    payload = json.dumps(config_json[switchport_list])
 
    # now we're in business, this is the final version of what we're about to push
    print(payload)
    
    # what you thought you'd get a chance to abort?
    # NOPE this is submitted about half a second before your brain even processed what was happening.
    # it is done.
    response = requests.request("PUT", url, data=payload, headers=headers)
    
    # this is what Meraki thought about what you've just done.
    # it should look like the current configuration of this interface, but if you get errors
    # you've clearly done something wrong
    print(response.text)

    # lastly we increment so we can do the next switchport in the next loop
    switchport_list += 1
