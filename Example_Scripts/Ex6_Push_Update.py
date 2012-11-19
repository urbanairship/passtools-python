# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example6: Updating installed passes in real-time with push
#
# This example assumes you've created a pass from a template that has
# at least one primary field and two secondary fields, all
# with default key names.
# Example is more interesting if you installed that pass on multiple phones.
#
# Copyright 2012, Tello, Inc.
##########################################

import copy
import logging

from passtools import pt_service

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: You must request an API key from Tello
api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always instantiate a service api object, providing your api key.
# This is required!
the_service = pt_service.Service(api_key)

# Pick the pass to work on
# This example script is more interesting if you installed that pass on multiple phones.
test_pass_id = your-pass-id-goes-here

# Retrieve the full form of that pass
test_pass = the_service.get_pass(test_pass_id)
print 25*"#"
print "Retrieved Pass #%s" % test_pass_id
print test_pass
print 25*"#"

# Now update the pass...
# Make a copy of the fields to operate on
temp_pass = copy.deepcopy(test_pass)

# modify fields here:
temp_pass.pass_fields["primary1"]["value"] = "ExcitingUpdate!"
temp_pass.pass_fields["secondary1"]["value"] = "ExcitingUpdate!"
temp_pass.pass_fields["secondary2"]["value"] = "ExcitingUpdate!"

# Call 'update', passing the modifications as input.
test_pass.update(temp_pass)

# Call 'push' to trigger updates of installed copies of the pass
return_data = test_pass.push_update()
print 25*"#"
print "Pushed Pass #%s" % test_pass_id
print return_data
print 25*"#"

# All done logging
logging.shutdown()

