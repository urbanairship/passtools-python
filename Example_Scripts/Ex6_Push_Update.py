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
# DON'T FORGET TO INSTALL THE PASS ON ONE OR MORE DEVICES OR THE PUSH WON'T SUCCEED
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import copy

from passtools import PassTools
from passtools.pt_pass import Pass

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
print 25*"#"
print "Retrieving Pass #%s" % test_pass_id
get_response = Pass.get(test_pass_id)

print "Retrieved Pass..."
print get_response
print 25*"#"

# Now update the pass...
# Make a copy of the fields to operate on
working_copy = copy.deepcopy(get_response["passFields"])

# modify fields here:
working_copy["primary1"]["value"] = "Push Happens!"
working_copy["secondary1"]["value"] = "Push Happens Again!"

# Call 'update', passing the modifications as input.
update_response = Pass.update(test_pass_id, working_copy)
print update_response

# Retrieve the updated form of that pass just to prove it was updated
get_response = Pass.get(test_pass_id)

print "Updated Pass..."
print get_response
print 25*"#"

print 25*"#"
print "Updated Pass #%s" % test_pass_id
print "After update, primary1 says:", get_response["passFields"]["primary1"]["value"]
print "After update, secondary1 says:", get_response["passFields"]["secondary1"]["value"]
print 25*"#"

# Call 'push' to trigger updates of installed copies of the pass
# At this point, if you created 'change messages' for your template, users with the target
# pass should see a notification on their phone.
# And, of course, viewing the pass should reveal updated information.
print 25*"#"
print "Pushing update to Pass #%s" % test_pass_id
return_data = Pass.push_update(test_pass_id)
print return_data
print 25*"#"
