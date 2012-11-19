# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example1: Working with Templates
#
# Copyright 2012, Tello, Inc.
##########################################

import logging
import sys
from passtools import pt_service, pt_template

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: You must request an API key from Tello
api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always instantiate a service api object, providing your api key.
# This is required!
the_service = pt_service.Service(api_key)

# The 'list' operation retrieves a list of all your templates.
# The retrieved items do not include the complete template.fields_model,
# but instead are intended to provide quick lookup info.
# Note the sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve list of all existing Templates owned by this user"
template_list = the_service.list_templates()
the_word = "template" + "s"*(len(template_list)!=1)
print "Got a list containing %d %s for this user!" % (len(template_list), the_word)
print ""
if len(template_list) > 0:
    print "The most recently-created is this:"
    print template_list[0]
print 25*"#"
print ""

# Now we'll use 'get_template' to retrieve the complete form of that latest template.
# You might retrieve a template, for example, in preparation for creating an pass.
existing_template_id_owned_by_self = template_list[0].id
print 25*"#"
print "Retrieve existing Template #%d" % existing_template_id_owned_by_self
the_retrieved_template = the_service.get_template(existing_template_id_owned_by_self)
print the_retrieved_template
print 25*"#"
print ""

# Or we can instantiate the template using its ID.
print 25*"#"
print "Instantiate Template #%d" % existing_template_id_owned_by_self
the_instantiated_template = pt_template.Template(existing_template_id_owned_by_self)
print the_instantiated_template
print 25*"#"
print ""

# Let's delete that template
print 25*"#"
print "Delete Template #%d" % existing_template_id_owned_by_self
the_instantiated_template.delete()
# Alternatively: the_service.delete_template(existing_template_id_owned_by_self)

# And then try to retrieve it:
print "Attempted to retrieve deleted template #%s" % existing_template_id_owned_by_self
try:
    the_retrieved_template = the_service.get_template(existing_template_id_owned_by_self)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"
print ""

# Finally, let's try to retrieve a template owned by someone else.
# This template doesn't belong to me, so I should see errors.
existing_template_owned_by_other = 220
print 25*"#"
print "Attempt to retrieve someone else's template"
try:
    the_retrieved_template = the_service.get_template(existing_template_owned_by_other)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"

# All done logging
logging.shutdown()

