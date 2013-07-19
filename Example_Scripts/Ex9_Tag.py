import copy
import sys
import time
from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template
from passtools.pt_tag import Tag

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "your-key-goes-in-here"
my_api_key = "test"
my_base_url="http://localhost:8080/v1";

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key, base_url = my_base_url)

# First, we'll use 'list' to retrieve a list of pass headers we own (in abbreviated format)
# Note that, as with templates, default sort order of the list is most-recent-first
# and default page-size = 10
print 25*"#"

list_response = Tag.list()

pagination = list_response['pagination']
print "Page size", pagination['pageSize']
print "Page number", pagination['page']
print "Order by", pagination['order']
print "Order direction", pagination['direction']
for item in list_response['tags']:
    print item
print 25*"#", "\n"


####
passes = Pass()
passes = passes.list()
print 25*"#", "\n"

for item in passes['passes']:
    print item

first_pass = passes['passes'][0]
print 25*"#", "\n"

pass_id = first_pass['id']
template_id = first_pass['templateId']

passes.up











