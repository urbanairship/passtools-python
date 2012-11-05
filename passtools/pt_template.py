##########################################
# pt_template.py
#
# Models PassTools Template
#
# Copyright 2012, Tello, Inc.
##########################################

"""
Define and provide methods for manipulating PassTools Template objects.

"""
try:
    import simplejson as json
except ImportError:
    import json

from pt_client import PassToolsClient

class Template(object):

    def __init__(self, template_id = None):
        """
        Init, optionally populate, new pt_template.Template instance
        If template_id and template_fields_model are supplied, will retrieve complete instance,
        else just create new empty instance.

        API call used is v1/template (GET)

        @type template_id: int
        @param template_id: ID of the desired template [Optional]
        @return: None
        """
        super(Template, self).__init__()
        self.api_client = PassToolsClient()
        self.id = template_id
        self.name = None
        self.description = None
        self.fields_model = {}
        if self.id:
            new_template = self.get(self.id)
            if new_template:
                self.name = new_template.name
                self.description = new_template.description
                self.fields_model = new_template.fields_model

    def __str__(self):
        pretty_template_fields = json.dumps(self.fields_model, sort_keys = True, indent = 2, encoding="ISO-8859-1")
        return "id=%s\nname=%s\ndescription:%s\nfields_model:%s" % (self.id,
                                                                    self.name,
                                                                    self.description,
                                                                    pretty_template_fields)

    def get(self, template_id = None):
        """
        Retrieve Template specified by template_id

        API call used is v1/template (GET)

        @type template_id: int
        @param template_id: ID of the desired template
        @return: pt_template. Template instance
        """
        if template_id is None: template_id = self.id
        if template_id is None:
            raise InvalidParameterException("get called without required parameter: template_id")
        try:
            test = float(template_id)
        except ValueError, TypeError:
            raise InvalidParameterException("get called with non-numeric parameter: template_id ('%s')" % template_id)

        new_template = None
        request_url = "/template/%s" % (str(template_id))
        response_code, response_data_dict = self.api_client.pt_get_dict(request_url)
        if response_code == 200:
            new_template = Template()
            new_template.id = int(response_data_dict["templateHeader"]["id"])
            new_template.name = response_data_dict["templateHeader"]["name"]
            new_template.description = response_data_dict["templateHeader"]["description"]
            new_template.fields_model = response_data_dict["fieldsModel"]
        return new_template

    def list(self):
        """
        Retrieve list of existing templates created by owner of API-key
        Note that list() returns abbreviated form of templates. Use get() to retrieve full template.

        API call used is v1/template/headers (GET)

        @return: List of pt_template.Template instances
        """
        template_list = []
        dict_list = []
        request_url = "/template/headers"
        response_code, response_data_dict = self.api_client.pt_get_dict(request_url)
        if response_code == 200:
            if "templateHeaders" in response_data_dict:
                dict_list = response_data_dict["templateHeaders"]
            for template_item in dict_list:
                new_template = Template()
                new_template.id = int(template_item["id"])
                new_template.name = template_item["name"]
                new_template.description = template_item["description"]
                new_template.fields_model = {}
                template_list.append(new_template)
        return template_list
