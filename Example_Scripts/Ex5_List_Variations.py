# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example5: Retrieving Template and Pass lists
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import sys

from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template

# Couple of utilities just to keep things tidier:
def report_templates(theList):
    print "Total count of templates for this user:", list_response['count']
    print "Page size", list_response['pageSize']
    print "Page number", list_response['page']
    print "Order by", list_response['orderField']
    print "Order direction", list_response['orderDirection']
    for item in list_response['templateHeaders']:
        print item

def report_passes(theList):
    print "Total count of passes for this user:", list_response['Count']
    print "Page size", list_response['PageSize']
    print "Page number", list_response['Page']
    print "Order by", list_response['OrderField']
    print "Order direction", list_response['OrderDirection']
    for item in list_response['Passes']:
        print item

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key)

#######################
# TEMPLATES:
#######################
# First, we'll demonstrate using 'list' to retrieve a default list of headers for templates we own
print 25*"#"
print "Retrieve default list of existing Templates owned by this user"
print "Note that the list is accompanied by some meta-info about total template count, page-size, etc."
print "And that the list of template headers proper is under the 'templateHeaders' key\n"

list_response = Template.list()
report_templates(list_response)
print 25*"#", "\n"

print "Alter pageSize, default sort"

list_response = Template.list(pageSize=3)
report_templates(list_response)
print 25*"#", "\n"

print "Alter pageSize, sort by name, ascending"
# By the way: available sort order keys are "name", "id", "created", and "updated"

list_response = Template.list(pageSize=7, direction="asc", order="Name")
report_templates(list_response)
print 25*"#", "\n"


#######################
# PASSES:
#######################
# Now a few examples with passes. Same methods hold.

# First, we'll use 'list' to retrieve a default list of passes we own (in abbreviated format)
# Note that, as with templates, default sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve default list of existing Passes owned by this user"
print "Note that the list is accompanied by some meta-info about total pass count, page-size, etc."
print "And that the list of pass descriptions proper is under the 'Passes' key\n"
print "Note also that you can retrieve passes associated with a specific template"

list_response = Pass.list()
report_passes(list_response)
print 25*"#", "\n"


print 25*"#"
print "Retrieve second page of existing Passes, 15 per page, owned by this user, ascending sort by creation date"
list_response = Pass.list(pageSize=15, page=2, direction="desc", order="created")
report_passes(list_response)
print 25*"#", "\n"

# Let's get passes associated with a specific template
# You would normally know which template ID you were interested in, but we'll just grab a known-good one
the_template_id = int(list_response["Passes"][-1]["templateId"])
print 25*"#"
print "Retrieve 2nd page of 3-per-page passes associated with template %s" % the_template_id
list_response = Pass.list(templateId = the_template_id, pageSize=3, page=2)
report_passes(list_response)
print 25*"#", "\n"

# Let's request passes associated with a non-existent template
the_template_id = 23456
print 25*"#"
print "Retrieve list of passes associated with non-existent template %s" % the_template_id
try:
    list_response = Pass.list(templateId = the_template_id)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#", "\n"
