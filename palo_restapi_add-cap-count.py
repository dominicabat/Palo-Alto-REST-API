import requests
from requests.auth import HTTPBasicAuth
import urllib3
import pprint
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#list the devices/hostnames here for the script to iterate login, for the sake of demonstration, I've listed the same firewall. But in usage, list all the IPs of the firewall here. 
devices = ['192.168.100.27', '192.168.100.27']

for device in devices:
    headers = {'Content-Type':'application/json'}
    #The example here queries the "location = vsys", this means it's querying the firewalls' locally created object not the panorama pushed. For example's and lab's sake, I would use the location=vsys 
    url_add = f"https://{device}/restapi/v10.1/Objects/Addresses?location=vsys&vsys=vsys1"
    url_addgrp = f"https://{device}/restapi/v10.1/Objects/AddressGroups?location=vsys&vsys=vsys1"
    url_edl = f"https://{device}/restapi/v10.1/Objects/ExternalDynamicLists?location=vsys&vsys=vsys1"
    #In production, I would change the API/URL to https://{device}/restapi/v10.1/Objects/ExternalDynamicLists?location=panorama-pushed, this would query the objects that came from panorama instead of the locally created ones. 


    #dyn_count is the number of Address Groups that are classified as Dynamic. Dynamic is the one counted (not static) when accounting for the total Address Capacity of the firewall. 
    dyn_count = 0
    stc_count = 0
    pa_220_capacity = 2500


    #define the https request and store them as dictionary value. This collects the Address, Address Gpoups, and EDL count of the firewall.
    response_add = requests.request("GET", url_add, headers=headers,verify=False,auth=HTTPBasicAuth('admin','123Cisco123'))
    response_dict_add = json.loads(response_add.text)

    response_grp = requests.request("GET", url_addgrp, headers=headers,verify=False,auth=HTTPBasicAuth('admin','123Cisco123'))
    response_dict_grp = json.loads(response_grp.text)

    response_edl = requests.request("GET", url_edl, headers=headers,verify=False,auth=HTTPBasicAuth('admin','123Cisco123'))
    response_dict_edl = json.loads(response_edl.text)


    #debug for add obj
    #pprint.pp(response_dict_add)
    #pprint.pp(int(response_dict_add['result']['@total-count']))
    #get the total count value, this corresponds to how many address objects are currently 
    total_address_obj = int(response_dict_add['result']['@total-count'])


    #debug for add groups
    #pprint.pp(response_dict_grp)
    #pprint.pp(response_dict_grp['result']['entry'])
    grp_list = response_dict_grp['result']['entry']

    for grp_item in grp_list:
        if "dynamic" in grp_item:
            #print("dynamic")
            dyn_count += 1
        else:
            #print("static")
            stc_count += 1


    #print (dyn_count)
    #print (stc_count)

    #pprint.pp(response_dict_edl)
    #pprint.pp(int(response_dict_edl['result']['@total-count']))
    total_EDL = int(response_dict_edl['result']['@total-count'])

    print(f"--------------------------------Checking {device}--------------------------------\n")
    print(f"the total address objects are: {total_address_obj}")
    print(f"the total number of Dynamic Address Groups are {dyn_count}")
    print (f"the total number of EDL is {total_EDL}")

    consumed_capacity = total_address_obj + dyn_count + total_EDL
    print (f"\nthe total address capacity consumed is {consumed_capacity}")

    percent_consumed = (consumed_capacity/pa_220_capacity)*100
    print (f"it's currently consumed {percent_consumed}%\n\n\n\n")