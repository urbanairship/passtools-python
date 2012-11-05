# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example3: Creating user-specific passes from a user DB
#
# In this example, we'll use a PassTools template to generate a set of passes, each of which is
# uniquely-created for one user from our customer DB. Of course, our example will be simple,
# but you have the freedom to create much more elaborate templates, and correspondingly-elaborate passes.
# For our example, we have prepared a basic 'generic' template (such as you might use for a club membership card.)
# In our template, we have added two secondary fields. We have given them custom keynames: 'fname' and 'lname'
# which are to contain the customer's first and last name, respectively.
# Our script, below, will generate the passes from our 'user DB', and download the passes so we can distribute them.
#
# Copyright 2012, Tello, Inc.
##########################################

import logging
from passtools import pt_service, pt_pass

# API User:
# STEP 1: You must request an API key from Tello
api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always instantiate a service api object, providing your api key.
# This is required!
the_service = pt_service.Service(api_key)

# Our model DB...
user_db = [{"first_name": "James", "last_name":"Bond"},
           {"first_name": "Jimi", "last_name":"Hendrix"},
           {"first_name": "Johnny", "last_name":"Appleseed"}]

# You'll have selected the template you want to use...you can find the template ID in the Template Builder UI
selected_template_id = 248

# Retrieve your template, so you can fill in the fields
the_template = the_service.get_template(selected_template_id)

# Now for each user in your DB, grab the user data, populate the template.fields_model, generate a pass and download it:
for user_record in user_db:
    the_template.fields_model["fname"]["value"] = user_record["first_name"]
    the_template.fields_model["lname"]["value"] = user_record["last_name"]
    new_pass = pt_pass.Pass(selected_template_id, the_template.fields_model)
    new_pass.download("/tmp/%s_%s.pkpass" % (user_record["first_name"], user_record["last_name"]))

# Now distribute the passes to your users!

# All done logging
logging.shutdown()

