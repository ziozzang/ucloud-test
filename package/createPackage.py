#!/usr/bin/python
# This code is sample of Creation of Package using Python Client.
# - Code by Jioh L. Jung (ziozzang@gmail.com)

import json
import UClient

import random
import string
import time
import sys
# -------------
# Functions
def get_randstr(length):
  char_set = string.ascii_lowercase + string.digits
  res = ''.join(random.sample(char_set*length,length))
  return res


# -------------
# Upload New Template

template_name = "%s" % get_randstr(6)
print "TEMPLATE NAME: %s" % template_name

# - Default Package Template Example
c = """
{
"Parameters": {
        "ZoneId": {
            "Description": "Available zoneId in ucloud",
            "Type": "String",
            "Default": "9845bd17-d438-4bde-816d-1b12f37d5080"
        }
},
"Resources": {
       
		"IpAddress": {
			"Type": "UPAC::IpAddress",
			"Properties": {
				"ZoneId": { "Ref" : "ZoneId" }
			}
		}
}
}
"""
if len(sys.argv) >= 2:
  c = open(sys.argv[1] ,"r").read().replace('\n','')
params = {
  "PackageName": template_name,
  #"DisableRollback" : "True",
  #"TemplateBody": c,
}
body = {
  #"TemplateName": template_name,
  "TemplateBody": c,
}

r = client.run("createPackage", params, post=body, resptype="xml",debug=True)
#r = client.run("uploadTemplate", params, debug=True)
#r = client.run("uploadTemplate", body, debug=True)
#r = client.run("uploadTemplate", params, post=body, debug=True)

print r
