##########################################
# pt_pass.py
#
# Models PassTools Pass
#
# Copyright 2012, Tello, Inc.
##########################################

"""
Define and provide methods for manipulating PassTools Pass objects.

"""

try:
    import simplejson as json
except ImportError:
    import json

from pt_client import PassToolsClient
from pt_exceptions import *

class Pass(object):

    def __init__(self, template_id = None, template_fields_model_dict = None):
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
        super(Pass, self).__init__()
        self.created_at = None
        self.pass_fields = None
        self.id = None
        self.template_id = None
        self.url = None
        self.api_client = PassToolsClient()
        if template_id and template_fields_model_dict:
            new_pass = self.create(template_id, template_fields_model_dict)
            if new_pass:
                self.created_at = new_pass.created_at
                self.pass_fields = json.loads(new_pass.pass_fields, encoding="ISO-8859-1")
                self.id = new_pass.id
                self.template_id = new_pass.template_id
                self.url = new_pass.url

    def __str__(self):
        pretty_pass_fields = json.dumps(self.pass_fields, sort_keys = True, indent = 2, encoding="ISO-8859-1")
        return "id: %s\ntemplate_id: %s\nurl: %s\npass_fields: %s" % (self.id,
                                                                        self.template_id,
                                                                        self.url,
                                                                        pretty_pass_fields)

    def __load_from_pass_dict(self, pass_dict):
        # Any unset fields will be assigned to corresponding value present in pass_json
        field_name_map = {"created_at":"createdAt", "pass_fields":"passFields",
                                                                "id":"id","template_id":"templateId", "url":"url"}
        for member_name in field_name_map:
            db_name = field_name_map[member_name]
            if member_name in vars(self) and not vars(self)[member_name] and db_name in pass_dict:
                vars(self)[member_name] = pass_dict[db_name]

    def create(self, template_id = None, template_fields_model_dict = None):
        """
        Create new Pass from specified template.

        API call used is v1/pass/<template_id> (POST)

        @type template_id: int
        @param template_id: ID of the template used to create new pass
        @type template_fields_model_dict: dict
        @param template_fields_model_dict: template_fields_model dict of the template used to create new pass
        @return: pt_pass.Pass instance
        """
        if template_id is None:
            raise InvalidParameterException("Pass.create() called without required parameter: template_id")
        try:
            test = float(template_id)
        except TypeError:
            raise InvalidParameterException("Pass.create() called with non-numeric parameter: template_id ('%s')" % template_id)
        if template_fields_model_dict is None:
            raise InvalidParameterException("Pass.create() called without required parameter: template_fields_model_dict")

        request_url = "/pass/%s" % (str(template_id))
        request_dict = {"json":json.dumps(template_fields_model_dict, encoding="ISO-8859-1")}
        response_code, response_data_dict = self.api_client.pt_post_dict(request_url, request_dict)

        new_pass = None
        if response_code == 200:
            new_pass = Pass()
            new_pass.pass_fields = json.dumps(template_fields_model_dict, encoding="ISO-8859-1")
            new_pass.template_id = template_id
            new_pass.__load_from_pass_dict(response_data_dict)

        return new_pass

    def update(self, update_fields = None):
        """
        Update existing pass

        API call used is v1/pass/<pass_id> (PUT)

        @type update_fields: dict
        @param update_fields: Pass.pass_fields dict
        @return: pt_pass.Pass instance
        """
        updated_pass = None
        if update_fields is None or update_fields.id is None:
            raise InvalidParameterException("Pass.update() called without required parameter: update_fields")

        request_url = "/pass/%s" % (str(self.id))
        request_dict = {"json":json.dumps(update_fields.pass_fields, encoding="ISO-8859-1")}
        response_code, response_data = self.api_client.pt_put(request_url, request_dict)
        if response_code == 200:
            updated_pass = self.get()
        return updated_pass

    def push_update(self, pass_id = None):
        """
        Update installed passes using push method

        API call used is v1/pass/<pass_id>/push (PUT)

        @type pass_id: int
        @param pass_id: ID of desired pt_pass.Pass. [Optional: If not supplied, = self.id]
        @return: Dict
        """
        ret_data = {}
        if pass_id is None: pass_id = self.id
        if pass_id is None:
            raise InvalidParameterException("Pass.push_update() called without required parameter: pass_id")
        try:
            test = float(pass_id)
        except TypeError:
            raise InvalidParameterException("Pass.push_update() called with non-numeric parameter: pass_id ('%s')" % pass_id)

        request_url = "/pass/%s/push" % (str(pass_id))
        response_code, response_data = self.api_client.pt_put(request_url)
        if response_code == 200:
            ret_data = response_data

        return ret_data

    def get(self, pass_id = None):
        """
        Retrieve existing pass with specified ID

        API call used is v1/pass/<pass_id> (GET)

        @type pass_id: int
        @param pass_id: ID of desired pt_pass.Pass. [Optional: If not supplied, = self.id]
        @return: pt_pass.Pass instance
        """
        if pass_id is None: pass_id = self.id
        if pass_id is None:
            raise InvalidParameterException("Pass.get() called without required parameter: pass_id")
        try:
            test = float(pass_id)
        except TypeError:
            raise InvalidParameterException("Pass.get() called with non-numeric parameter: pass_id ('%s')" % pass_id)

        request_url = "/pass/%s" % (str(pass_id))
        response_code, response_data_dict = self.api_client.pt_get_dict(request_url)

        new_pass = None
        if response_code == 200:
            new_pass = Pass()
            new_pass.__load_from_pass_dict(response_data_dict)

        return new_pass

    def count(self, template_id = None):
        """
        Retrieve count of existing passes created by owner of API-key
        If template_id is specified, count only passes associated with that template

        API call used is v1/pass (GET)

        @type templateId: int
        @param templateId: ID of the template used to create new pass
        @return: Integer
        """
        request_dict = {}
        if template_id:
            request_dict["templateId"] = template_id
        request_url = "/pass"
        response_code, response_data_dict = self.api_client.pt_get_dict(request_url, request_dict)

        ret_val = 0
        if response_code == 200:
            ret_val = int(response_data_dict["Count"])

        return ret_val

    def list(self, **kwargs):
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
        @return: List of pt_pass.Pass instances
        """

        request_dict = kwargs
        request_url = "/pass"
        response_code, response_data_dict = self.api_client.pt_get_dict(request_url, request_dict)

        pass_list = []
        if response_code == 200:
            for pass_dict in response_data_dict["Passes"]:
                new_pass = Pass()
                new_pass.__load_from_pass_dict(pass_dict)
                pass_list.append(new_pass)

        return pass_list

    def download(self, destination_path = None, pass_id = None):
        """
        Download pkpass file corresponding to existing pass with specified ID

        API call used is v1/pass/<pass_id>/download (GET)

        @type destination_path: str
        @param destination_path: path to receive pass file. Path must exist, and filename must end with ".pkpass"
        @type pass_id: int
        @param pass_id: pass_id of pt_pass.Pass instance desired  [Optional: If not supplied, = self.id]
        """
        if pass_id is None:
            pass_id = self.id
        try:
            test = float(pass_id)
        except TypeError:
            raise InvalidParameterException("Pass.download() called with non-numeric parameter: pass_id ('%s')" % pass_id)
        if destination_path is None:
            raise InvalidParameterException("Pass.download() called without required parameter: destination_path")

        request_url = "/pass/%s/download" % (str(pass_id))
        response_code, response_data = self.api_client.pt_get_json(request_url)

        if response_code == 200:
            fh = open(destination_path, "wb")
            fh.write(response_data)
            fh.close()

    def delete(self, pass_id = None):
        """
        delete existing pass

        API call used is v1/pass/<pass_id> (DELETE)

        @type pass_id: int
        @param pass_id: ID of the pass to delete [Optional: If not supplied, = self.id]
        @return: None
        """
        if pass_id is None:
            pass_id = self.id
        try:
            test = float(pass_id)
        except TypeError:
            raise InvalidParameterException("Pass.delete() called with non-numeric parameter: pass_id ('%s')" % pass_id)

        request_url = "/pass/%s" % (str(pass_id))
        response_code, response_data = self.api_client.pt_delete(request_url, {})
        if response_code == 200:
            self.created_at = None
            self.pass_fields = None
            self.id = None
            self.template_id = None
            self.url = None
            self.api_client = PassToolsClient()
