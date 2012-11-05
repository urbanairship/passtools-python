##########################################
# pt_service.py
#
# Models PassTools Service
#
# Copyright 2012, Tello, Inc.
##########################################

"""
Models PassTools Service, providing access to the PassTools API.

"""
from pt_client import PassToolsClient
from pt_template import Template
from pt_pass import Pass

class Service(object):

    def __init__(self, my_api_key):
        """
        Init new pt_service.Service instance

        @type my_api_key: str
        @param my_api_key: User-specific API key required for accessing PassTools API
        @return: None
        """
        super(Service, self).__init__()
        # Share the current api_key with all importers of the module
        global api_key
        api_key = my_api_key.encode('utf8')
        self.api_client = PassToolsClient()

    def is_service_up(self):
        """
        Make an HTTP request to status URL

        API call used is v1/pass/system/status (GET)

        @return: True if HTTP response was 200
        """
        request_url = "/system/status"
        response_code, response_data = self.api_client.pt_get_json(request_url)
        return response_code == 200

    def get_template(self, template_id = None):
        """
        Retrieve Template specified by template_id

        API call used is v1/template (GET)

        @type template_id: int
        @param template_id: ID of the desired template
        @return: pt_template.Template instance
        """
        new_template = Template(template_id)
        return new_template

    def list_all_templates(self):
        """
        Retrieve list of existing templates created by owner of API-key
        Note that list() returns abbreviated form of templates. Use get() to retrieve full template.

        API call used is v1/template/headers (GET)

        @return: List of pt_template.Template instances
        """
        temp_template = Template()
        return temp_template.list()

    def create_pass(self, template_id = None, template_fields_model_dict = None):
        """
        Create new Pass from specified template.

        API call used is v1/pass/<template_id> (POST)

        @type template_id: int
        @param template_id: ID of the template used to create new pass
        @type template_fields_model_dict: dict
        @param template_fields_model_dict: template_fields_model dict of the template used to create new pass
        @return: pt_pass.Pass instance
        """
        new_pass = Pass(template_id, template_fields_model_dict)
        return new_pass

    def update_pass(self, update_fields = None):
        """
        Update existing pass

        API call used is v1/pass/<pass_id> (PUT)

        @type update_fields: dict
        @param update_fields: template_fields_model dict of the template used to create new pass
        @return: pt_pass.Pass instance
        """
        temp_pass = Pass()
        return temp_pass.update_pass(update_fields)

    def get_pass(self, pass_id = None):
        """
        Retrieve existing pass with specified ID

        API call used is v1/pass/<pass_id> (GET)

        @type pass_id: int
        @param pass_id: ID of desired pt_pass.Pass.
        @return: pt_pass.Pass instance
        """
        new_pass = Pass(pass_id)
        return new_pass

    def list_all_passes(self):
        """
        Retrieve list of existing passes created by owner of API-key
        Note that list() returns abbreviated form of passes. Use get() to retrieve full pass.

        API call used is v1/pass (GET)

        @return: List of pt_pass.Pass instances
        """
        temp_pass = Pass()
        return temp_pass.list()

    def download_pass(self, destination_path = None, pass_id = None):
        """
        Download pkpass file corresponding to existing pass with specified ID

        API call used is v1/pass/<pass_id>/download (GET)

        @type pass_id: int
        @param pass_id: pass_id of pt_pass.Pass instance desired
        @type destination_path: str
        @param destination_path: path to receive pass file. Path must exist, and filename must end with ".pkpass"
        """
        temp_pass = Pass()
        return temp_pass.download(destination_path, pass_id)
