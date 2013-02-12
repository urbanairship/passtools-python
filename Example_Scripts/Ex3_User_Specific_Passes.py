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
# Copyright 2013, Urban Airship, Inc.
##########################################

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

# Our model DB...
user_db = [{"first_name": "James", "last_name":"Bond"},
           {"first_name": "Jimi", "last_name":"Hendrix"},
           {"first_name": "Johnny", "last_name":"Appleseed"}]

# You'll have selected the template you want to use...you can find the template ID in the Template Builder UI
selected_template_id = 604

# Retrieve your template, so you can fill in the fields
the_template = Template.get(selected_template_id)

# Now for each user in your DB, grab the user data, populate the template.fields_model, generate a pass and download it:
for user_record in user_db:
    the_template.fields_model["fname"]["value"] = user_record["first_name"]
    the_template.fields_model["lname"]["value"] = user_record["last_name"]
    new_pass = Pass.create(selected_template_id, the_template.fields_model)
    Pass.download(new_pass.id,
                  "/tmp/%s_%s.pkpass" % (user_record["first_name"], user_record["last_name"]))

# Now distribute the passes to your users!

# All done logging
logging.shutdown()

