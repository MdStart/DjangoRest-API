import requests
import json
a=requests.get("https://183.82.41.58:9443/vsphere-client/",auth=('root','Nexii@123'), verify=False)
print a.headers
print a.text
