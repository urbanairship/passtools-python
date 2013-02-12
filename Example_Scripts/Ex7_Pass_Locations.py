# -*- coding: ISO-8859-1 -*-
##########################################
# Using the PassTools API
# Example7: Adding and deleting Relevant Locations from passes
#
# In general, the PassTools API expects to operate on passes generated from templates
# in which NO Relevant Locations have been defined.
#
# The presumption is that users who wish to create relatively small numbers of passes
# for which the Relevant Locations are all the same will use the UI, and define Relevant
# Locations in their templates, whereas users who wish to generate large numbers of
# passes with unique Relevant Locations will define and add Relevant Locations on a
# per-pass basis, using the API. This example follows that idea, and so makes the
# simplifying assumption that the pass was created from a template for which
# no Relevant Locations were defined.
#
# When working with Relevant Locations, keep in mind that the rules
# are pass-type-dependent. More detail is available in PassTools docs, but a brief summary:
#
# Relevant Locations can consist of up to 3 components:
# Relevant Date, Relevant Location, Relevant Text.
# There is a maximum of 1 Relevant Date per template/pass.
# There is a maximum of 10 Relevant Locations per template/pass.
# Each location can, but need not, have an associated Relevant Text.
#
# Coupon and StoreCard passes ignore Relevant Date, so their rules are simplest:
# If a Relevant Location is specified for a pass installed on an iOS device, and that
# device is near* the Relevant Location, a notification will be presented on the
# device lock screen. If a Relevant Text was defined for that Location, that text will
# be used as the notification, otherwise the notification will be simply "Nearby."
#
# Event Tickets are sensitive to Relevant Date, or the pairing of Relevant Date and
# Relevant Location. So, if the pass includes only a Relevant Date, and that date
# matches* the current date/time, the notification will be a system-defined string of the
# form, "Today at 12:30 P.M." If the pass includes both Relevant Date and Relevant Location
# information, than notification will only be displayed if _both_ match. If a Relevant Text
# was defined for the Location, that text will be used as the notification, otherwise
# the notification will be simply "Nearby."
#
# Generic passes are in a way the converse of Event tickets: A Relevant Date can be used only
# when one or more Relevant Locations have been defined. If a pass includes only Relevant Location
# data, then notifications will fire if the iOS device is near the target location. If
# Relevant Date has also been defined, then notifications will be displayed when the device
# is near the target location at about the target date/time.
#
# Finally, Boarding Passes can include either Relevant Locations, Relevant Date, or both.
# If only one of the other is present, that data will control display of notifications.
# If both are present, notifications will display when both pieces of data match current
# conditions.
#
# *Both distance and time matches are registered for agreement within some measurement
# plus/minus some allowance defined by Apple.
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

# Let's create a new pass from a template.
# Start by retrieving a template using the same method used in Ex1_Templates.py
# The first two steps are a bit contrived, since you would know the ID of the template
# you wanted to use, but for this example we'll get the whole list and use the latest
template_list = Template.list()
the_template_id = template_list[0].id

the_template = Template.get(the_template_id)

# Now create a new pass from the template.
test_pass = Pass.create(the_template_id, the_template.fields_model)

print 25*"#"
print "New Pass at start"
print test_pass
print 25*"#"

# Add a location to that pass. Locations are passed as a list of dicts, length 1 or more
# A pass can have a maximum of 10 locations
print 25*"#"
print "Adding locations to new pass..."
location_list_1=[{"latitude":37.4471107, "longitude":-122.16206219999998,
                    "streetAddress1":"408 Florence St", "streetAddress2":"",
                    "city":"Palo Alto", "region":"CA", "regionCode":"94301",
                    "country":"US", "relevantText":"Palo Alto Office!"}]
Pass.add_locations(test_pass.id, location_list_1)
print "After adding 1 location..."
after_first_add = Pass.get(test_pass.id)
print after_first_add
print 25*"#"

# Add multiple locations at one time
print 25*"#"
print "Adding locations to new pass..."
location_list_2 =[{"latitude":45.5255003, "longitude":-122.6821440,
                   "streetAddress1":"334 NW 11th Ave", "streetAddress2":"",
                   "city":"Portland", "region":"OR", "regionCode":"97209",
                   "country":"US", "relevantText":"Portland Office!"},
                  {"latitude":37.7723721, "longitude":-122.4057149,
                   "streetAddress1":"41 Decatur", "streetAddress2":"",
                   "city":"San Francisco", "region":"CA", "regionCode":"94103",
                   "country":"US", "relevantText":"SF Office!"}]
Pass.add_locations(test_pass.id, location_list_2)
print "After adding 2 more locations..."
after_second_add = Pass.get(test_pass.id)
print after_second_add
print 25*"#"

# Locations are deleted from a pass individually, and addresses by ID
# Keep in mind: passes may have two sets of locations: "passLevel" and "templateLevel"
# "passLevel" locations are those added directly to a pass (via the API)
# "templateLevel" locations can be thought of as "default" locations inserted via the UI at template-creation
# ONLY PASSLEVEL LOCATIONS CAN BE DELETED VIA THE API
# As noted above, if you're intending to modify pass locations via the API, it is expected (and suggested)
# that you NOT install locations into templates via the UI.
print 25*"#"
location_ids = []
print "Deleting locations from pass..."
the_pass_dict = after_second_add.pass_dict
if "passLocationFields" in the_pass_dict:
    if "passLevel" in the_pass_dict["passLocationFields"]:
        for loc_record in the_pass_dict["passLocationFields"]["passLevel"]:
            location_ids.append(loc_record["id"])
print "location_ids", location_ids
for location_id in location_ids:
    print "deleting %s" % location_id
    test_pass.delete_location(test_pass.id, location_id)
    print "After location deletion"
    after_deletion = Pass.get(test_pass.id)
    print after_deletion
print 25*"#"

# All done logging
logging.shutdown()
