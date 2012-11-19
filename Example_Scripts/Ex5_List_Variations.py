# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example5: Retrieving Pass and Template lists
#
# Copyright 2012, Tello, Inc.
##########################################

import logging
import sys

from passtools import pt_service

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)

# API User:
# STEP 1: You must request an API key from Tello
api_key = "your-key-goes-in-here"

# STEP 2:
# You'll always instantiate a service api object, providing your api key.
# This is required!
the_service = pt_service.Service(api_key)

#######################
# TEMPLATES:
#######################
# First, we'll use 'list' to retrieve a default list of templates we own (in abbreviated format)
# Default sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve default list of existing Templates owned by this user"
the_list = the_service.list_templates()
the_word = "template" + "s"*(len(the_list)!=1)
print "Got a list of %d %s owned by this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here's the first element in the list:"
    print the_list[0]
print 25*"#"

# We can get a count of all templates owned by this user
print 25*"#"
print "Count existing Templates owned by this user"
template_count = the_service.count_templates()
the_word = "template" + "s"*(template_count!=1)
print "This user owns %d %s!" % (template_count, the_word)
print 25*"#"

print 25*"#"
retrieve_count = 3
print "Retrieve list of up to %d existing Templates owned by this user, default sort" % retrieve_count
the_list = the_service.list_templates(pageSize=retrieve_count)
the_word = "template" + "s"*(len(the_list)!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    for item in the_list:
        print item.id
print 25*"#"

print 25*"#"
retrieve_count = 3
print "Retrieve list of up to %d existing Templates owned by this user, default sort" % retrieve_count
the_list = the_service.list_templates(pageSize=retrieve_count, direction="asc")
the_word = "template" + "s"*(template_count!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here's the first one in the list:"
    print the_list[0]
    print "And the last one:"
    print the_list[-1]
print 25*"#"

print 25*"#"
retrieve_count = 3
print "Retrieve list of up to %d existing Templates owned by this user, default sort" % retrieve_count
the_list = the_service.list_templates(pageSize=retrieve_count, direction="desc")
the_word = "template" + "s"*(template_count!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here's the first one in the list:"
    print the_list[0]
    print "And the last one:"
    print the_list[-1]
print 25*"#"

print 25*"#"
retrieve_count = 9
print "Retrieve list of up to %d existing Templates owned by this user, ascending sort by name" % retrieve_count
the_list = the_service.list_templates(pageSize=retrieve_count, order="Name", direction="ASC")
the_word = "template" + "s"*(template_count!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    if len(the_list) > 0:
        for item in the_list:
            print "Item #%d...Name: %s" % (item.id, item.name)
print 25*"#"

#######################
# PASSES:
#######################

# First, we'll use 'list' to retrieve a default list of passes we own (in abbreviated format)
# Note that, as with templates, default sort order of the list is most-recent-first.
print 25*"#"
print "Retrieve default list of existing Passes owned by this user"
the_list = the_service.list_passes()
the_word = "pass" + "es"*(len(the_list)!=1)
print "Got a list of %d %s owned by this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here's the first element of the list: (remember that 'pass_fields' will be None for items returned by 'list')"
    print the_list[0]
print 25*"#"

# We can get a count of all passes owned by this user
print 25*"#"
print "Count existing Passes owned by this user"
pass_count = the_service.count_passes()
the_word = "pass" + "es"*(pass_count!=1)
print "This user owns %d %s!" % (pass_count, the_word)
print 25*"#"

# Or a count of passes this owner created associated with a specific template
the_template_id = int(the_list[0].template_id)
print 25*"#"
print "Count existing Passes owned by this user, generated from template %d" % the_template_id
pass_count = the_service.count_passes(the_template_id)
the_word = "pass" + "es"*(pass_count!=1)
print "This user owns %d %s associated with that template!" % (pass_count, the_word)
print 25*"#"

# Now let's retrieve a list of up to 35 passes (in abbreviated format), and reverse the sort order
print 25*"#"
print "Retrieve list of 35 existing Passes owned by this user, reverse sort"
the_list = the_service.list_passes(pageSize=35, direction="asc")
the_word = "pass" + "es"*(len(the_list)!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here's the first element of the list:"
    print the_list[0]
    print "And the last one:"
    print the_list[-1]
print 25*"#"

# Let's get passes...3 per page, second page, default order
print 25*"#"
print "Retrieve 2nd page of 3-per-page passes"
the_list = the_service.list_passes(pageSize=3, page=2)
the_word = "pass" + "es"*(len(the_list)!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here they are:"
    for item in the_list:
        print item
print 25*"#"

# Let's get passes associated with a specific template...3 per page, second page, default order
the_template_id = the_list[-1].template_id
print 25*"#"
print "Retrieve 2nd page of 3-per-page passes associated with template %s" % the_template_id
the_list = the_service.list_passes(templateId = the_template_id, pageSize=3, page=2)
the_word = "pass" + "es"*(len(the_list)!=1)
print "Got a list of %d %s for this user!" % (len(the_list), the_word)
if len(the_list) > 0:
    print "Here they are:"
    for item in the_list:
        print item
print 25*"#"

# Let's get passes associated with a non-existent template
the_template_id = 23456
print 25*"#"
print "Retrieve list of passes associated with non-existent template %s" % the_template_id
try:
    the_list = the_service.list_passes(templateId = the_template_id)
except:
    info = sys.exc_info()
    print info[1]
print 25*"#"

# All done logging
logging.shutdown()

