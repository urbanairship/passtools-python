# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
#
# PURPOSE:
# Update a pass and push changes in real-time to passes installed and in the field.
# Generally, that is the technique used with the PassTools API for push updates:
# First update a pass, then call push with that pass ID.
#
# PREPARATION:
# Prior to execution, create a template which includes at least
# one Primary field (named "primary1") and one secondary (named "secondary1")
# It's even more fun if you add change messages for those fields.
# Generate a pass from that template.
# Install that pass on one or more phones, and use the ID of that pass in the script below.
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import copy
import logging

from passtools import PassTools
from passtools.pt_pass import Pass

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key)

# Pick the pass to work on
# This example script is more interesting if you installed that pass on multiple phones.
test_pass_id = your-pass-id-goes-here

# Retrieve the full form of that pass
test_pass = Pass.get(test_pass_id)
print 25*"#"
print "Retrieved Pass #%s" % test_pass_id
print "Initially, primary1 says:", test_pass.pass_dict["passFields"]["primary1"]["value"]
print "Initially, secondary1 says:", test_pass.pass_dict["passFields"]["secondary1"]["value"]
print 25*"#"

# Update the pass...
# Make a copy of the fields to operate on
working_copy = copy.deepcopy(test_pass.pass_dict["passFields"])

# modify fields here:
working_copy["primary1"]["value"] = "Push Happens!"
working_copy["secondary1"]["value"] = "Push Happens!"

# Call 'update', passing the modifications as input.
updated_pass = Pass.update(test_pass.id, working_copy)

print 25*"#"
print "Updated Pass after update #%s" % updated_pass.id
print "After update, primary1 says:", updated_pass.pass_dict["passFields"]["primary1"]["value"]
print "After update, secondary1 says:", updated_pass.pass_dict["passFields"]["secondary1"]["value"]
print 25*"#"

# Retrieve the updated form of that pass
retrieved_pass = Pass.get(updated_pass.id)
print 25*"#"
print "Retrieved Pass #%s" % retrieved_pass.id
print "Retrieved after update, primary1 says:", retrieved_pass.pass_dict["passFields"]["primary1"]["value"]
print "Retrieved after update, secondary1 says:", retrieved_pass.pass_dict["passFields"]["secondary1"]["value"]
print 25*"#"

# Call 'push' to trigger updates of installed copies of the pass
# At this point, if you created 'change messages' for your template, users with the target
# pass should see a notification on their phone.
# And, of course, viewing the pass should reveal updated information.
print 25*"#"
print "Pushing update to Pass #%s" % updated_pass.id
return_data = Pass.push_update(updated_pass.id)
print return_data
print 25*"#"

# All done logging
logging.shutdown()