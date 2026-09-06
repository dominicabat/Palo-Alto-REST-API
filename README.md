# Palo-Alto-REST-API
repository of my code for scripting and programmability for Palo Alto via REST API

## Description
This project was made to explore Palo Alto's REST API automation

## Modules Needed
```
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import csv
import pprint
import json
```

## Code Documentation / Thought Process 
[Technical Blog / Article](https://medium.com/@dominusabat/palo-alto-rest-api-address-capacity-count-0b2854b91951)

## Update the list of devices through device_list.csv
```
hostname_001,192.168.100.27
hostname_002,192.168.100.28
```

## Define cred for auth
```
admin
p4ss
```

## Execute the script
```
py palo_restapi_add-cap-count.py
```

# Author
[John Dominic Abat](https://github.com/dominicabat/)
