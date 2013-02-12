# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example2: Working with Passes
#
# PREPARATION:
# For this script to run as intended, you should
# create a new template just before running. That template should
# have at least one primary field (named "primary1") and
# one secondary field (named "user_first_name").
# And you should have created one pass from that template.
#
# Copyright 2013, Urban Airship, Inc.
##########################################

import copy
import logging
import sys

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

# First, we'll use 'list' to retrieve a list pass headers we own (in abbreviated format)
# Note that, as with templates, default sort order of the list is most-recent-first
# and default page-size = 10
print 25*"#"
print "Retrieve list of Passes owned by this user"
pass_list = Pass.list()
the_word = "pass" + "es"*(len(pass_list)!=1)
print "Got a list of %d %s for this user!" % (len(pass_list), the_word)
if len(pass_list) > 0:
    print "Here's the most recent one: (remember that 'pass_fields' will be None for items returned by 'list')"
    print pass_list[0]
print 25*"#"

# Next, we'll retrieve the full form of that pass
# You might retrieve a pass, for example, in preparation for updating it.
print 25*"#"
latest_pass_id = pass_list[0].id
print "Retrieving Pass #%s" % latest_pass_id
the_retrieved_pass = Pass.get(latest_pass_id)
print the_retrieved_pass
print 25*"#"

# Now let's create a new pass from a template.
# Start by retrieving a template using the same method used in Ex1_Templates.py
# The first two steps are a bit contrived, since you would probably know the ID of the template
# you wanted to use, but for this example we'll get the whole list and use the latest
print "listing templates"
template_list = Template.list()
the_template_id = template_list[0].id
print "Latest template id:", the_template_id

the_template = Template.get(the_template_id)

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


print 25*"#"
print "Creating new Pass from template ID %s" % the_template_id
new_pass = Pass.create(the_template_id, the_template.fields_model)
print new_pass
print 25*"#"

# There are a few ways to deliver passes to customers (and more to come), several of which involve you distributing
# the pass file itself...so you'll want to download passes you create.
# Let's do that, using the 'download' method of a pass.
# IMPORTANT: you'll want to be sure to give your passes the '.pkpass' extension, or they will not be properly recognized
# when your customer receives them.
print 25*"#"
print "Downloading an id-specified Pass from the service..."
Pass.download(new_pass.id, "/tmp/New_Pass_2.pkpass")
print 25*"#"

# Next, we'll update an existing pass, using--surprise!--the 'update' method. In this case, we use the fields
# from the existing pass, modify them, and call update. In typical usage, you might call 'get' above to retrieve a
# pass to use as input...we'll the pass we just created, so the script output will allow you to compare before/after update.
# Make a copy of the fields to operate on

pass_fields = copy.deepcopy(new_pass.pass_dict["passFields"])
print 25*"#"
print "Start pass update test..."
# modify fields here...as an example:
if "primary1" in pass_fields:
    pass_fields["primary1"]["value"] = "Updated Primary!"
else:
    print "No primary1 to update"
if "relevantDate" in pass_fields:
    pass_fields["relevantDate"]["value"] = "2013-01-30T18:30-08:00"
else:
    print "No relevantDate to update"

# Call 'update', passing the modifications as input.
updated_pass = Pass.update(new_pass.id, pass_fields)

print "Updated Pass..."
print updated_pass
print 25*"#"
# The update will be returned; note that the ID is the same, the serial number is the same,
# and any changes you passed in have been incorporated.
# If you send the updated pass to a user who has already installed the previous version,
# they'll see an "Update" button instead of an "Add" button in the iOS UI.

print 25*"#"
print "Downloading updated pass..."
ret_val = Pass.download(new_pass.id, "/tmp/Updated_Pass.pkpass")
print "ret_val from download", ret_val
print 25*"#"

# Finally, let's delete the pass:
print 25*"#"
deleted_id = updated_pass.id
print "Delete Pass %s" % deleted_id
ret_val = Pass.delete(deleted_id)
print "ret_val from delete:", ret_val

# And then try to retrieve it:
print "Attempted to retrieve deleted pass #%s" % deleted_id
try:
    the_retrieved_pass = Pass.get(deleted_id)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"

# All done logging
logging.shutdown()

