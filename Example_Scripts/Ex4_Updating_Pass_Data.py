# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example4: Updating fields on passes
#
# PURPOSE:
# In this example, we'll imagine a time-sensitive Coupon: it includes (in our simplified version)
# an offer, and an expiration date. After each expiration date, we'll send an update; the update
# replaces the old Coupon, and includes a new offer and a new expiration date.
#
# PREPARATION:
# For this example, we prepared a Coupon template, and sent a pass to start from.
# We gave a custom key name to the Primary field--we call it "offer".
# We also gave a custom key name to a Secondary field: "exp_date".
# Our is a pretty boring template, but you are free to update any/all fields you define in your templates.
# Just keep in mind that if you mark a field as "Required," you _must_ pass it in when you update, and if you
# mark a field as "Don't show if empty" then if you update without data for a given field, it won't appear.
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

# Retrieve the current form of the pass, using the pass ID.
current_pass_id = 2039
starting_pass = Pass.get(current_pass_id)

# Let's a copy of the fields to operate on
pass_fields = copy.deepcopy(starting_pass["passFields"])

print "Starting:"
print "Offer:", pass_fields["offer"]["value"]
print "Exp_date:", pass_fields["exp_date"]["value"]

# Now set the new data. We're going to imagine that our initial offer just expired, and we're setting a '15% off'
# offer to extend 'til the end of the year:

# NOTE: date values must be passed in iso-8601 format
pass_fields["exp_date"]["value"] = "2013-01-01T12:01Z"
pass_fields["offer"]["value"] = "15% Off!!!"

# Call 'update', passing the modifications as input
update_response = Pass.update(current_pass_id, pass_fields)
print update_response

# At this point, you could retrieve the updated pass, download it, etc.
updated_pass = Pass.get(current_pass_id)

pass_fields = copy.deepcopy(updated_pass["passFields"])

print "After update:"
print "Offer:", pass_fields["offer"]["value"]
print "Exp_date:", pass_fields["exp_date"]["value"]
