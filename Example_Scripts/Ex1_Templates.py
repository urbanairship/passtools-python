# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example1: Working with Templates
#
# Copyright 2013, Urban Airship, Inc.
##########################################

try:
    import simplejson as json
except ImportError:
    import json
import sys

from passtools import PassTools
from passtools.pt_template import Template
from testdata import TestData

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "test"
my_base_url="http://localhost:8080/v1";

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key, base_url =  my_base_url)

print "################test##################"

template = Template()
test_data = TestData()
template_dict = {'name' : 'py_test_template', 'description' : 'py_template_desc', 'type': 'boardingPass', 'projectType': 'boardingPass', 'vendor':'Apple'}
headers = test_data.template_headers
fields = test_data.template_fields
#headers = '{"headers" : {"test" : "hello"}}'
headers_dict = json.loads(headers)
fields_dict = json.loads(fields)
response = Template.create(template_info_dict=template_dict,headers_dict=headers_dict, fields_dict=fields_dict)

print "##############endtest"

# The 'list' operation retrieves a list of headers of templates created by the user referenced by the api_key.
# As headers, the retrieved items do not include the complete template.fields_model,
# but instead are intended to provide quick lookup info.
# Note the default sort order of the list is most-recent-first, and default page size = 10.

print 25*"#"
print "Retrieve default list of existing Templates owned by this user"
print "Note that the list is accompanied by some meta-info about total template count, page-size, etc."
print "And that the list of template headers proper is under the 'templateHeaders' key\n"

list_response = Template.list()
print "Total count of templates for this user:", list_response['count']
pagination = list_response['pagination']
print "Page size", pagination['pageSize']
print "Page number", pagination['page']
print "Order by", pagination['order']
print "Order direction", pagination['direction']

for item in list_response['templateHeaders']:
    print item
print 25*"#", "\n"

# Use get() to retrieve the full form of one template--we'll just use the last ID in the list above.
# You might retrieve a template, for example, in preparation for creating an pass.
print 25*"#"
the_template_id = int(list_response['templateHeaders'][0]["id"])
print "Retrieve existing Template #%d" % the_template_id
get_response = Template.get(the_template_id)

the_template = Template()
the_template.header = get_response["templateHeader"]
the_template.fields_model = get_response["fieldsModel"]
print the_template
print 25*"#","\n"

# Delete that template
print 25*"#"
print "Delete Template #%d" % the_template_id
Template.delete(the_template_id)

# And then try to retrieve it:
print "Attempted to retrieve deleted template #%s" % the_template_id
try:
    get_response = Template.get(the_template_id)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"
print ""

# Finally, let's try to retrieve a template owned by someone else,
# to demonstrate the expected error
template_id_owned_by_other = 220
print 25*"#"
print "Attempt to retrieve someone else's template"
try:
    get_response = Template.get(template_id_owned_by_other)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"


#create template example



template = Template();
template_dict = {'name' : 'py_test_template', 'description' : 'py_template_desc', 'type': 'boardingPass', 'projectType': 'boardingPass', 'vendor':'Apple'}
headers = TestData.template_headers
fields = TestData.template_fields
header_dict = json.loads(headers)
fields_dict = json.loads(fields)
template.create(template_info_dict=template_dict,header_dict=header_dict, fields_dict=fields_dict)
