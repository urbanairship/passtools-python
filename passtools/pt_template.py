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

import urllib
import pt_client

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
        @return: json form of template full-form description
        """
        request_url = "/template/%s" % int(template_id)
        return pt_client.pt_get(request_url)

    @classmethod
    def get_by_external_id(cls, template_external_id):
        """

        @param cls:
        @param template_external_id:
        @return:
        """
        request_url = "/template/id/%s" % template_external_id
        return pt_client.pt_get(request_url)


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
        @return: json form of list of template header descriptions
        """
        request_dict = kwargs
        request_url = "/template/headers"
        return pt_client.pt_get(request_url, request_dict)

    @classmethod
    def delete(cls, template_id):
        """
        delete existing template

        API call used is v1/template/<template_id> (DELETE)

        @type template_id: int
        @param template_id: ID of the template to delete
        @return: json form of response data
        """

        request_url = "/template/%d" % int(template_id)
        return pt_client.pt_delete(request_url, {})

    @classmethod
    def delete_by_external_id(cls, template_external_id):
        """

        @param cls:
        @param template_external_id:
        @return:
        """
        request_url = "/template/id/%d" % template_external_id
        return pt_client.pt_delete(request_url, {})


    @classmethod
    def __create__(cls, request_url, template_info_dict, headers_dict, fields_dict):
        result_dict = {}
        result_dict.update(template_info_dict)
        result_dict.update(headers_dict);
        result_dict.update(fields_dict);
        request_dict = {"json": json.dumps(result_dict, encoding="ISO-8859-1")}
        request_url = "/template"
        return pt_client.pt_post(request_url, request_dict)

    @classmethod
    def create(cls, template_info_dict, headers_dict, fields_dict, project_id = None):
        """

        @param cls:
        @param template_info_dict:
        @param headers_dict:
        @param fields_dict:
        @param project_id
        @return:
        """
        request_url = "/template"
        if project_id is not None:
            request_url += "/%d" % int(project_id)
        return cls.__create__(request_url, template_info_dict, headers_dict, fields_dict)

    @classmethod
    def create_by_external_id(cls,external_id, template_info_dict, headers_dict, fields_dict, project_id=None):
        """

        @param cls:
        @param external_id:
        @param template_info_dict:
        @param header_dict:
        @param fields_dict:
        @return:
        """
        request_url = "/template"
        if project_id is not None:
            request_url += "/id/%d" % int(project_id)
        request_url += "/id/%s" % urllib.quote_plus(external_id)
        return cls.__create__(request_url, template_info_dict, headers_dict, fields_dict)




    @classmethod
    def duplicate(cls, template_id):
        """

        @param cls:
        @param template_id:
        @return:
        """
        request_url = "/template/duplicate/%d" % int(template_id)
        return pt_client.pt_post(request_url,{})


    @classmethod
    def duplicate_by_external_id(cls, template_external_id):
        """

        @param cls:
        @param template_external_id:
        @return:
        """
        request_url = "/template/duplicate/id/%s" % urllib.quote_plus(template_external_id)
        return pt_client.pt_post(request_url,{})
