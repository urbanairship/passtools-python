# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example8: Updating the "RelevantDate" field
#
# For this script to run as intended, you should
# create a new template just before running.
# That template should include a "Relevant Date".
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import copy
import logging

from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key)

# Let's create a new pass from a template.
# Start by retrieving a template using the same method used in Ex1_Templates.py
# This is a bit contrived, since you would probably know the ID of the template
# you wanted to use, but for this example we'll get the whole list and use the latest
template_list = Template.list()
the_template_id = template_list[0].id

the_template = Template.get(the_template_id)

# Now create a new pass from the template.
new_pass = Pass.create(the_template_id, the_template.fields_model)

print 25*"#"
print "New Pass before update"
print new_pass
print 25*"#"

# And let's update the "relevantDate" field in that pass
# Note that as of this writing, the RelevantDate argument is not format-validated
# so you _must_ ensure that the date you pass in confirms to ISO-8601
pass_fields = copy.deepcopy(new_pass.pass_dict["passFields"])
print 25*"#"
print "Start pass update..."
if "relevantDate" in pass_fields:
    pass_fields["relevantDate"]["value"] = "2012-01-01T12:00-08:00"

    # Call 'update', passing the modifications as input.
    updated_pass = Pass.update(new_pass.id, pass_fields)

    print "Updated Pass..."
    print updated_pass
    print 25*"#"
    # The update will be returned; note that the ID is the same, the serial number is the same,
    # and the change to RelevantDate has been incorporated.

else:
    print "No relevantDate to update"


# All done logging
logging.shutdown()

