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
import sys

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

# First, we'll use 'list' to retrieve a list of pass headers we own (in abbreviated format)
# Note that, as with templates, default sort order of the list is most-recent-first
# and default page-size = 10
print 25*"#"
print "Retrieve default list of existing Passes owned by this user"
print "Note that the list is accompanied by some meta-info about total pass count, page-size, etc."
print "And that the list of pass descriptions proper is under the 'Passes' key\n"
print "Note also that you can retrieve passes associated with a specific template"

list_response = Pass.list()
print "Total count of passes for this user:", list_response['Count']
print "Page size", list_response['PageSize']
print "Page number", list_response['Page']
print "Order by", list_response['OrderField']
print "Order direction", list_response['OrderDirection']
for item in list_response['Passes']:
    print item
print 25*"#", "\n"

# Next, we'll retrieve the full form of a pass
# You might retrieve a pass, for example, in preparation for updating it.
# Normally, you'd know the ID of the pass you wanted--we'll just grab an id from the list above
print 25*"#"
the_pass_id = int(list_response['Passes'][0]['id'])

print "Retrieving Pass #%s" % the_pass_id
get_response = Pass.get(the_pass_id)

print "Retrieved Pass..."
print get_response
print 25*"#"

# Now let's create a new pass from a template.
# Start by retrieving a template using the same method used in Ex1_Templates.py
# The first two steps are a bit contrived, since you would probably know the ID of the template
# you wanted to use, but for this example we'll get the whole list and use the latest
list_response = Template.list()
the_template_id = int(list_response['templateHeaders'][0]["id"])
get_response = Template.get(the_template_id)
the_template_fields_model = get_response["fieldsModel"]

# With the template in hand, you could modify any values for fields you defined in that template, so
# that the modifications would appear in the pass you create
# As an example, you might change a primary field value
# Here's one using a default key name:
#    the_template_fields_model["primary1"]["value"] = "10% Off!"
# And in this one, we set 'user_first_name' as a custom key name when we created the template
#    the_template_fields_model["user_first_name"]["value"] = "John"

# Keep in mind:
#   - If you marked a field as "Required", you'll have to give it a value here, unless you gave it a default
#   - If you marked a field as 'Don't show if empty', then if you don't give it a value here, it won't show on the pass

# Now create a new pass from the template.
# Of course, we haven't changed any fields (since we don't know what's in your template!),
# so this pass will look like the template, but by changing the fields as described above,
# you'll be able to generate one form for many customers, or a unique pass for each customer, or anything in between.

print 25*"#"
print "Creating new Pass from template ID %s" % the_template_id
create_response = Pass.create(the_template_id, the_template_fields_model)
print create_response
print 25*"#"

# There are a few ways to deliver passes to customers (and more to come), several of which involve you distributing
# the pass file itself...so you'll want to download passes you create.
# Let's do that, using the 'download' method of a pass.
# IMPORTANT: you'll want to be sure to give your passes the '.pkpass' extension, or they will not be properly recognized
# when your customer receives them.
print 25*"#"
new_pass_id = create_response['id']
print "Downloading an id-specified Pass from the service..."
Pass.download(new_pass_id, "/tmp/New_Pass.pkpass")
print 25*"#"

# Next, we'll update an existing pass, using--surprise!--the 'update' method. In this case, we use the fields
# from the existing pass, modify them, and call update. In typical usage, you might call 'get' above to retrieve a
# pass to use as input...we'll the pass we just created, so the script output will allow you to compare before/after update.
# Make a copy of the fields to operate on

pass_fields = copy.deepcopy(create_response["passFields"])
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
update_response = Pass.update(new_pass_id, pass_fields)
print "Response from pass update..."
print update_response

get_response = Pass.get(update_response['id'])

print "Updated Pass..."
print get_response
# Note that, after the update, the ID is the same, the serial number is the same,
# and any changes you passed in have been incorporated.
# If you send the updated pass to a user who has already installed the previous version,
# they'll see an "Update" button instead of an "Add" button in the iOS UI.

# Btw, you can instantiate a Pass, which gives you some convenience features like pretty-print:
updated_pass = Pass()
updated_pass.pass_dict = get_response

print "Updated pass as object"
print updated_pass
print 25*"#"

# Passes can be downloaded, so you can distribute them via email, for example
print 25*"#"
print "Downloading updated pass..."
ret_val = Pass.download(new_pass_id, "/tmp/Updated_Pass.pkpass")
print "ret_val from download", ret_val
print 25*"#"

# Finally, let's delete a pass:
print 25*"#"
print "Delete Pass %s" % new_pass_id
ret_val = Pass.delete(new_pass_id)
print "ret_val from delete:", ret_val

# And then try to retrieve it:
print "Attempted to retrieve deleted pass #%s" % new_pass_id
try:
    the_retrieved_pass = Pass.get(new_pass_id)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"
