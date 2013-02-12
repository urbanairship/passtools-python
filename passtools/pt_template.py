##########################################
# pt_template.py
#
# Models PassTools Template
#
# Copyright 2013, Urban Airship, Inc.
##########################################

"""
Define and provide methods for manipulating PassTools Template objects.

"""
try:
    import simplejson as json
except ImportError:
    import json

from passtools import PassTools

class Template(object):

    def __init__(self, template_id = None):
        """
        Init, optionally populate, new pt_template.Template instance
        If template_id is supplied, will retrieve complete instance,
        otherwise just create new empty instance.

        API call used is v1/template (GET)

        @type template_id: int
        @param template_id: ID of the desired template [Optional]
        @return: None
        """
        self.header = {}
        self.fields_model = {}
        if template_id:
            new_template = self.get(template_id)
            if new_template:
                self.header = new_template.header
                self.fields_model = new_template.fields_model

    @property
    def id(self):
        the_id = None
        if self.header and "id" in self.header:
            the_id = int(self.header["id"])
        return the_id

    def __str__(self):
        pretty_header_fields = json.dumps(self.header, sort_keys = True, indent = 2, encoding = "ISO-8859-1")
        pretty_template_fields = json.dumps(self.fields_model, sort_keys = True, indent = 2, encoding = "ISO-8859-1")
        return "header:%s\nfields_model:%s" % (pretty_header_fields, pretty_template_fields)

    @classmethod
    def get(cls, template_id):
        """
        Retrieve full-form template specified by template_id

        API call used is v1/template/<template_id> (GET)

        @type template_id: int
        @param template_id: ID of the template to retrieve
        @return: pt_template.Template instance
        """
        request_url = "/template/%s" % (str(template_id))
        response_code, response_data_dict = PassTools.request_client.pt_get_dict(request_url)

        new_template = None
        if response_code == 200:
            new_template = Template()
            new_template.header = response_data_dict["templateHeader"]
            new_template.fields_model = response_data_dict["fieldsModel"]

        return new_template

    @classmethod
    def list(cls, **kwargs):
        """
        Retrieve list of existing templates created by owner of API-key
        Optional parameters are translated into query-modifiers

        Note that list() returns header-only form of templates. Use get() to retrieve full template.

        API call used is v1/template/headers (GET)

        @type pageSize: int
        @param pageSize: Maximum length of list to return [Optional; Default = 10]
        @type page: int
        @param page: 1-based index of page into list, based on page_size [Optional; Default = 1]
        @type order: string
        @param order: Name of field on which to sort list [Optional; From (ID, Name, Created, Updated)]
        @type direction: string
        @param direction: Direction which to sort list [Optional; From (ASC, DESC); Default = DESC]
        @return: List of pt_template.Template instances
        """
        request_dict = kwargs
        request_url = "/template/headers"
        response_code, response_data_dict = PassTools.request_client.pt_get_dict(request_url, request_dict)

        template_list = []
        if response_code == 200:
            dict_list = []
            if "templateHeaders" in response_data_dict:
                dict_list = response_data_dict["templateHeaders"]
            for header_dict in dict_list:
                new_template = Template()
                new_template.header = header_dict
                template_list.append(new_template)

        return template_list

    @classmethod
    def delete(cls, template_id):
        """
        delete existing template

        API call used is v1/template/<template_id> (DELETE)

        @type template_id: int
        @param template_id: ID of the template to delete
        @return: Response data
        """

        request_url = "/template/%s" % (str(template_id))
        response_code, response_data = PassTools.request_client.pt_delete(request_url, {})

        return response_data

