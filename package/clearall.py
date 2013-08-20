#!/usr/bin/python
# UCloud Package Clean up utility.
# - this code need ucloud python client.
# - Code by Jioh L. Jung (ziozzang@gmail.com)

import json
import UClient

import random
import string
import time


client = UClient.UClient(api_type="package")

def get_pkg_property(template_id):
  r = client.run("listPackages")
  for i in r['listpackagesresult']['packagesummaries']:
    if i['packagesummary']['packagename'] == template_id:
      return i['packagesummary']
  return None


def remove_package_all():
  r = client.run("listPackages")
  for i in r['listpackagesresult']['packagesummaries']:
      pkg_name = i['packagesummary']['packagename']
      pkg_status = i['packagesummary']['packagestatus']
      print "Removing Package : %s" % pkg_name
      if pkg_status == 'DELETE_FAILED':
        print " >> DELETE Failed."
        continue
      params = {
        "PackageName": pkg_name,
      }
      q = client.run("deletePackage", params)
      
      while True:
        found = get_pkg_property(pkg_name)
        if found is None:
          print " Package is Deleted!"
          break
        elif found['packagestatus'] == 'DELETE_FAILED':
          print " DELETE Failed!"
          break
        else:
          print "."
        time.sleep(1)
      

def remove_template_all():
  r = client.run("listTemplates")
  for i in r['listtemplatesresult']['templatesummaries']:
      template_id = i['templatesummary']['templateid']
      print "Removing Template : %s" % template_id
      q = client.run("deleteTemplate", {"TemplateId": template_id })


remove_package_all()
remove_template_all()
