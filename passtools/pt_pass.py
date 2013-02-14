##########################################
# pt_pass.py
#
# Models PassTools Pass
#
# Copyright 2013, Urban Airship, Inc.
##########################################

"""
Define and provide methods for manipulating PassTools Pass objects.

"""

try:
    import simplejson as json
except ImportError:
    import json

import pt_client
from passtools import PassTools


class Pass(object):
    def __init__(self, template_id=None, template_fields_model_dict=None):
        """
        Init, optionally populate, new pt_pass.Pass instance
        If template_id and template_fields_model are supplied, will create new complete instance,
        else just create empty instance.
        
        API call used is v1/pass/<template_id> (POST)
        
        @type template_id: int
        @param template_id: ID of the template used to create new pass [Optional]
        @type template_fields_model_dict: dict
        @param template_fields_model_dict: template_fields_model dict of the template used to create new pass [Optional]
        @return: None
        """
        self.pass_dict = None
        if template_id and template_fields_model_dict is not None:
            new_pass = self.create(template_id, template_fields_model_dict)
            if new_pass:
                self.pass_dict = new_pass.pass_dict

    @property
    def id(self):
        the_id = None
        if self.pass_dict and "id" in self.pass_dict:
            the_id = int(self.pass_dict["id"])
        return the_id

    @property
    def template_id(self):
        the_id = None
        if self.pass_dict and "template_id" in self.pass_dict:
            the_id = self.pass_dict["template_id"]
        return the_id

    def __str__(self):
        return json.dumps(self.pass_dict, sort_keys=True, indent=2, encoding="ISO-8859-1")

    @classmethod
    def create(cls, template_id, template_fields_model_dict):
        """
        Create new Pass from specified template.

        API call used is v1/pass/<template_id> (POST)

        @type template_id: int
        @param template_id: ID of the template used to create new pass
        @type template_fields_model_dict: dict
        @param template_fields_model_dict: template_fields_model dict of the template used to create new pass
        @return: json form of template full-form description
        """

        request_url = "/pass/%d" % int(template_id)
        request_dict = {"json": json.dumps(template_fields_model_dict, encoding="ISO-8859-1")}
        return pt_client.pt_post(request_url, request_dict)

    @classmethod
    def update(cls, pass_id, update_fields):
        """
        Update existing pass

        API call used is v1/pass/<pass_id> (PUT)

        @type pass_id: int
        @param pass_id: ID of desired Pass
        @type update_fields: dict
        @param update_fields: Pass.pass_dict dict
        @return: json form of template full-form description
        """

        request_url = "/pass/%d" % int(pass_id)
        request_dict = {"json": json.dumps(update_fields, encoding="ISO-8859-1")}
        return pt_client.pt_put(request_url, request_dict)

    @classmethod
    def push_update(cls, pass_id):
        """
        Update installed passes using push method

        API call used is v1/pass/<pass_id>/push (PUT)

        @type pass_id: int
        @param pass_id: ID of desired Pass
        @return: Response data
        """

        request_url = "/pass/%d/push" % int(pass_id)
        return pt_client.pt_put(request_url)

    @classmethod
    def get(cls, pass_id):
        """
        Retrieve existing pass with specified ID

        API call used is v1/pass/<pass_id> (GET)

        @type pass_id: int
        @param pass_id: ID of desired Pass
        @return: json form of template full-form description
        """

        request_url = "/pass/%d" % int(pass_id)
        return pt_client.pt_get(request_url, {})

    @classmethod
    def list(cls, **kwargs):
        """
        Retrieve list of existing passes created by owner of API-key
        If template_id is specified, retrieve only passes associated with that template
        Other parameters are translated into query-modifiers

        Note that list() returns abbreviated form of passes. Use get() to retrieve full pass.

        API call used is v1/pass (GET)

        @type templateId: int
        @param templateId: ID of the template used to create new pass
        @type pageSize: int
        @param pageSize: Maximum length of list to return [Optional; Default = 10]
        @type page: int
        @param page: 1-based index of page into list, based on page_size [Optional; Default = 1]
        @type order: string
        @param order: Name of field on which to sort list [Optional; From (ID, Name, Created, Updated)]
        @type direction: string
        @param direction: Direction which to sort list [Optional; From (ASC, DESC); Default = DESC]
        @return: json form of list of pass header descriptions
        """

        request_dict = kwargs
        request_url = "/pass"
        return pt_client.pt_get(request_url, request_dict)

    @classmethod
    def download(cls, pass_id, destination_path):
        """
        Download pkpass file corresponding to existing pass with specified ID

        API call used is v1/pass/<pass_id>/download (GET)

        @type pass_id: int
        @param pass_id: ID of desired Pass
        @type destination_path: str
        @param destination_path: path to receive pass file. Path must exist, and filename must end with ".pkpass"
        @return: Writes pass to filesystem
        """

        request_url = "/pass/%d/download" % int(pass_id)
        resp = pt_client.pt_get(request_url)
        if PassTools.test_mode:
            return resp
        elif resp is not None:
            fh = open(destination_path, "wb")
            fh.write(resp.content)
            fh.close()

    @classmethod
    def delete(cls, pass_id):
        """
        delete existing pass

        API call used is v1/pass/<pass_id> (DELETE)

        @type pass_id: int
        @param pass_id: ID of Pass to delete
        @return: json form of response data
        """

        request_url = "/pass/%d" % int(pass_id)
        return pt_client.pt_delete(request_url, {})

    @classmethod
    def add_locations(cls, pass_id, location_list):
        """
        add locations to an existing pass

        API call used is v1/pass/<pass_id>/locations (POST)

        @type pass_id: int
        @param pass_id: ID of the pass to add locations to
        @type location_list: list
        @param location_list: list of locations to add
        @return: json form of response data
        """

        request_url = "/pass/%d/locations" % int(pass_id)
        request_dict = {"json": json.dumps(location_list, encoding="ISO-8859-1")}
        return pt_client.pt_post(request_url, request_dict)

    @classmethod
    def delete_location(cls, pass_id, location_id):
        """
        delete existing location from pass

        API call used is v1/pass/<pass_id>/location/<location_id> (DELETE)

        @type pass_id: int
        @param pass_id: ID of the pass to delete from
        @type location_id: int
        @param location_id: ID of the location to delete
        @return: json form of response data
        """

        request_url = "/pass/%d/location/%d" % (int(pass_id), int(location_id))
        return pt_client.pt_delete(request_url, {})
