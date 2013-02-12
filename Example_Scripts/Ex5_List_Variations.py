# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example5: Retrieving Template and Pass lists
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import logging
import sys

from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# Couple of utilities just to keep things tidier:
def report_templates(theList):
    print "Got a list containing %d template%s for this user!\n" % (len(the_list), "s"*(len(the_list)!=1))

def report_passes(theList):
    print "Got a list containing %d pass%s for this user!\n" % (len(the_list), "es"*(len(the_list)!=1))


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
# First, we'll use 'list' to retrieve a default list of templates we own (in abbreviated format)
# Default sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve default list of existing Templates owned by this user"
the_list = Template.list()
report_templates(the_list)
if len(the_list) > 0:
    print "Here's the first element in the list:"
    print the_list[0]
print 25*"#", "\n"

print 25*"#"
retrieve_count = 3
print "Retrieve list of up to %d existing Templates owned by this user, default sort" % retrieve_count
the_list = Template.list(pageSize=retrieve_count)
report_templates(the_list)
if len(the_list) > 0:
    for item in the_list:
        print item.id
print 25*"#", "\n"

print 25*"#"
retrieve_count = 3
print "Retrieve list of up to %d existing Templates owned by this user, _ascending_ sort" % retrieve_count
the_list = Template.list(pageSize=retrieve_count, direction="asc")
report_templates(the_list)
if len(the_list) > 0:
    print "Here's the first one in the list:"
    print the_list[0]
    print "And the last one:"
    print the_list[-1]
print 25*"#", "\n"

print 25*"#"
retrieve_count = 3
print "Retrieve list of up to %d existing Templates owned by this user, _descending_ sort" % retrieve_count
the_list = Template.list(pageSize=retrieve_count, direction="desc")
report_templates(the_list)
if len(the_list) > 0:
    print "Here's the first one in the list:"
    print the_list[0]
    print "And the last one:"
    print the_list[-1]
print 25*"#", "\n"

print 25*"#"
retrieve_count = 9
print "Retrieve list of up to %d existing Templates owned by this user, ascending sort by name" % retrieve_count
the_list = Template.list(pageSize=retrieve_count, order="Name", direction="asc")
report_templates(the_list)
if len(the_list) > 0:
    if len(the_list) > 0:
        for item in the_list:
            print "Item #%d...Name: %s" % (item.id, item.header["name"])
print 25*"#", "\n"

#######################
# PASSES:
#######################

# First, we'll use 'list' to retrieve a default list of passes we own (in abbreviated format)
# Note that, as with templates, default sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve default list of existing Passes owned by this user"
the_list = Pass.list()
report_passes(the_list)
if len(the_list) > 0:
    print "Here's the first element of the list: (remember that 'pass_fields' will be None for items returned by 'list')"
    print the_list[0]
print 25*"#", "\n"

# Now let's retrieve a list of up to 35 passes (in abbreviated format), and reverse the sort order
print 25*"#"
print "Retrieve list of 35 existing Passes owned by this user, reverse sort"
the_list = Pass.list(pageSize=35, direction="asc")
report_passes(the_list)
if len(the_list) > 0:
    print "Here's the first element of the list:"
    print the_list[0]
    print "And the last one:"
    print the_list[-1]
print 25*"#", "\n"

# Let's get passes...3 per page, second page, default order
print 25*"#"
print "Retrieve 2nd page of 3-per-page passes"
the_list = Pass.list(pageSize=3, page=2)
report_passes(the_list)
if len(the_list) > 0:
    print "Here they are:"
    for item in the_list:
        print item
print 25*"#", "\n"

# Let's get passes associated with a specific template...3 per page, second page, default order
the_template_id = int(the_list[-1].pass_dict["templateId"])
print 25*"#"
print "Retrieve 2nd page of 3-per-page passes associated with template %s" % the_template_id
the_list = Pass.list(templateId = the_template_id, pageSize=3, page=2)
report_passes(the_list)
if len(the_list) > 0:
    print "Here they are:"
    for item in the_list:
        print item
print 25*"#", "\n"

# Let's get passes associated with a non-existent template
the_template_id = 23456
print 25*"#"
print "Retrieve list of passes associated with non-existent template %s" % the_template_id
try:
    the_list = Pass.list(templateId = the_template_id)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#", "\n"

# All done logging
logging.shutdown()

