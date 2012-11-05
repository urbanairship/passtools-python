# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example2: Working with Passes
#
# Copyright 2012, Tello, Inc.
##########################################

import logging
import copy
from passtools import pt_service, pt_pass

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: You must request an API key from Tello
api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always instantiate a service api object, providing your api key.
# This is required!
the_service = pt_service.Service(api_key)

# First, we'll use 'list' to retrieve a list of all templates we own (in abbreviated format)
# Note that, as with templates, the sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve list of all existing Templates owned by this user"
pass_list = the_service.list_all_passes()
the_word = "pass" + "es"*(len(pass_list)!=1)
print "Got a list of %d %s for this user!" % (len(pass_list), the_word)
if len(pass_list) > 0:
    print "Here's the most recent one: (remember that pass_fields will be None for items returned by 'list')"
    print pass_list[0]
print 25*"#"

# Next, we'll retrieve the full form of that pass
# You might retrieve a pass, for example, in preparation for updating it.
the_retrieved_pass = the_service.get_pass(pass_list[0].id)
print 25*"#"
print "Retrieved Pass #%s" % pass_list[0].id
print the_retrieved_pass
print 25*"#"

# Now let's create a new pass from a template.
# Start by retrieving a template using the same method used in Ex1_Templates.py
# The first two steps are a bit contrived, since you would probably know the ID of the template
# you wanted to use, but for this example we'll get the whole list and use the latest
template_list = the_service.list_all_templates()
the_template_id = template_list[0].id

the_template = the_service.get_template(the_template_id)

# With the template in hand, you could modify any values for fields you defined in that template, so
# that the modifications would appear in the pass you create
# As an example, you might change a primary field value
# Here's one using a default key name:
#    the_template.fields_model["primary1"]["value"] = "10% Off!"
# And in this one, we set 'user_first_name' as a custom key name when we created the template
#    the_template.fields_model["user_first_name"]["value"] = "John"

# Keep in mind:
#   - If you marked a field as "Required", you'll have to give it a value here, unless you gave it a default
#   - If you marked a field as 'Don't show if empty', then if you don't give it a value here, it won't show on the pass

# Now create a new pass from the template.
# Of course, we haven't changed any fields (since we don't know what's in your template!),
# so this pass will look like the template, but by changing the fields as described above,
# you'll be able to generate one form for many customers, or a unique pass for each customer, or anything in between.
new_pass = pt_pass.Pass(the_template_id, the_template.fields_model)

print 25*"#"
print "New Pass"
print new_pass
print 25*"#"

# There are a few ways to deliver passes to customers (and more to come), several of which involve you distributing
# the pass file itself...so you'll want to download passes you create.
# Let's do that, using the 'download' method of a pass.
# IMPORTANT: you'll want to be sure to give your passes the '.pkpass' extension, or they will not be properly recognized
# when your customer receives them.
print 25*"#"
print "Downloading a Pass from an instance..."
new_pass.download("/tmp/New_Pass.pkpass")
print 25*"#"

# Alternatively, the pt_service class can download passes specified by ID
print 25*"#"
print "Downloading an id-specified Pass from the service..."
the_service.download_pass("/tmp/New_Pass.pkpass", new_pass.id)
print 25*"#"

# Finally, we'll update an existing pass, using--surprise!--the 'update' method. In this case, we use the fields
# from the existing pass, modify them, and call update. In typical usage, you might call 'get' above to retrieve a
# pass to use as input...we'll the pass we just created, so the script output will allow you to compare before/after update.
# Make a copy of the fields to operate on
temp_pass = copy.deepcopy(new_pass)

# modify fields here...as an example:
#     temp_pass.pass_fields["primary1"]["value"] = "Updated Primary!"

# Call 'update', passing the modifications as input.
updated_pass = new_pass.update(temp_pass)
print 25*"#"
print "Updated Pass..."
print updated_pass
print 25*"#"
# The update will be returned; note that the ID is the same, the serial number is the same,
# and any changes you passed in have been incorporated.
# If you send the updated pass to a user who has already installed the previous version,
# they'll see an "Update" button instead of an "Add" button in the iOS UI.

# All done logging
logging.shutdown()

