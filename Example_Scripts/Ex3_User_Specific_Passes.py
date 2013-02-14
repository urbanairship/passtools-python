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

from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template

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

# Retrieve your template, so you can modify the data and create passes from it
get_response = Template.get(selected_template_id)

the_fields_model = get_response["fieldsModel"]

# Now for each user in your DB, grab the user data, modify the template.fields_model, create a pass and download it:
for user_record in user_db:
    the_fields_model["fname"]["value"] = user_record["first_name"]
    the_fields_model["lname"]["value"] = user_record["last_name"]

    create_response = Pass.create(selected_template_id, the_fields_model)

    new_pass_id = create_response["id"]
    print "NEW PASS CREATED. ID: %s, First: %s, Last: %s" % (new_pass_id, user_record["first_name"], user_record["last_name"])
    Pass.download(new_pass_id, "/tmp/%s_%s.pkpass" % (user_record["first_name"], user_record["last_name"]))

# Now distribute the passes to your users!
