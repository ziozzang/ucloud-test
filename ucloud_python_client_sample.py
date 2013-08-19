#!/usr/bin/python

import json
import UClient

import random
import string
import time

# -------------
# Parameters
API_KEY = "API_KEY_HERE"
SECRET = "SECRET_KEY_HERE"

# -------------
# Functions
def get_randstr(length):
  char_set = string.ascii_lowercase + string.digits
  res = ''.join(random.sample(char_set*length,length))
  return res



# -------------
# List Templates
client = UClient.UClient(api_type="package", api_key=API_KEY, secret=SECRET)
r = client.run("listTemplates", {})
print r


# -------------
# Upload New Template

template_name = "test01%s" % get_randstr(12)
print "TEMPLATE NAME: %s" % template_name
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
} }
"""
params = {
  "TemplateName": template_name,
}
body = {
  "TemplateBody": c,
}
r = client.run("uploadTemplate", params, post=body)
template_id = r['uploadtemplateresult']['templateid']

# -------------
# List Uploaded Template Check
r = client.run("listTemplates")
found = False
for i in r['listtemplatesresult']['templatesummaries']:
  if i['templatesummary']['templateid'] == template_id:
    print "> templatename: %s" % i['templatesummary']['templatename']
    print "> templateid: %s" % i['templatesummary']['templateid']
    break

# -------------
# Package List Check
def pkg_exist_check(template_id):
  r = client.run("listPackages")
  res = False
  for i in r['listpackagesresult']['packagesummaries']:
    if i['packagesummary']['packageid'] == template_id:
      res = True
      break
  return res

found = pkg_exist_check(template_id)
if found == False:
  print "Test Passed.."
else:
  print "Test Failed.."

# -------------
# Package Execute
params = {
  "TemplateId" : template_id,
  "PackageName": template_name,
}
r = client.run("createPackage", params)
package_id = r['createpackageresult']['packageid']

# -------------
# Get Package Status
def pkg_create_check(pkg_name):
  r = client.run("describePackages", {"PackageName": pkg_name})
  return r['describepackagesresult']['packages'][0]['package']['packagestatus']

while True:
  res = pkg_create_check(template_name)
  print " >> ", res
  if res == 'CREATE_COMPLETE':
    break
  time.sleep(5)

# -------------
# Package Resource
r = client.run("listPackageResources", {"PackageName": template_name})
print r

# -------------
# Remove Package
params = {
  "PackageName": template_name,
}
r = client.run("deletePackage", params)

# -------------
# Remove Package Status
while True:
  found = pkg_exist_check(template_id)
  if found:
    print " >> Package EXIST!"
  else:
    print " >> Package Deleted!"
    break
  time.sleep(5)

# -------------
# Remove Template

r = client.run("deleteTemplate", {"TemplateId": template_id })
print r
