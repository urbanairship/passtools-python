# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example4: Updating fields on passes
#
# In this example, we'll imagine a time-sensitive Coupon: it includes (in our simplified version)
# an offer, and an expiration date. After each expiration date, we'll send an update; the update
# replaces the old Coupon, and includes a new offer and a new expiration date.
#
# For this example, we prepared a Coupon template.
# We gave a custom key name to the Primary field--we call it "offer".
# We also gave a custom key name to a Secondary field: "exp_date".
# Our is a pretty boring template, but you are free to update any/all fields you define in your templates.
# Just keep in mind that if you mark a field as "Required," you _must_ pass it in when you update, and if you
# mark a field as "Don't show if empty" then if you update without data for a given field, it won't appear.
#
# Copyright 2012, Tello, Inc.
##########################################

import copy
import logging
from passtools import pt_service

# API User:
# STEP 1: You must request an API key from Tello
api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always instantiate a service api object, providing your api key.
# This is required!
the_service = pt_service.Service(api_key)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# Retrieve the current form of the pass, using the pass ID.
current_pass_id = your_pass_number_here
current_pass = the_service.get_pass(current_pass_id)

# Let's a copy of the fields to operate on
pass_copy = copy.deepcopy(current_pass)

# Now set the new data. We're going to imagine that our November offer just expired, and we're setting a '15% off'
# offer to extend 'til the end of the year:

pass_copy.pass_fields["exp_date"]["value"] = "12/31/12"
pass_copy.pass_fields["offer"]["value"] = "15% Off!!!"

# Call 'update', passing the modifications as input
updated_pass = current_pass.update(pass_copy)
# Alternatively use this form:
#updated_pass = the_service.update_pass(current_pass_id, pass_copy)

# Now download the updated pass, and distribute to your users!
the_service.download_pass("/tmp/DecemberOffer.pkpass", updated_pass.id)
# Alternatively use this form:
# updated_pass.download("/tmp/DecemberOffer.pkpass")

# All done logging
logging.shutdown()

