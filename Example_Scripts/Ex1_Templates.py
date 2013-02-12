# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example1: Working with Templates
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import logging
import sys

from passtools import PassTools
from passtools.pt_template import Template

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key)

# The 'list' operation retrieves a list of headers of templates created
# by the user referenced by the api_key.
# As headers, the retrieved items do not include the complete template.fields_model,
# but instead are intended to provide quick lookup info.
# Note the default sort order of the list is most-recent-first, and default page size = 10.
print 25*"#"
print "Retrieve list of existing Templates owned by this user"
template_list = Template.list()
print "Got a list containing %d %s for this user!\n" % (len(template_list), "template" + "s"*(len(template_list)!=1))
if len(template_list) > 0:
    print "The most recently-created is this:"
    print template_list[0]
print 25*"#","\n"

# Use get() to retrieve the full form of that template.
# The return will be an instantiated Template.
# You might retrieve a template, for example, in preparation for creating an pass.
template_id = template_list[0].id
print 25*"#"
print "Retrieve existing Template #%d" % template_id
the_retrieved_template = Template.get(template_id)
print the_retrieved_template
print 25*"#"
print ""

# Delete that template
print 25*"#"
print "Delete Template #%d" % template_id
Template.delete(template_id)

# And then try to retrieve it:
print "Attempted to retrieve deleted template #%s" % template_id
try:
    the_retrieved_template = Template.get(template_id)
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
    the_retrieved_template = Template.get(template_id_owned_by_other)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"

# All done logging
logging.shutdown()

