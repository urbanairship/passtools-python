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

    def __init__(self, my_api_key, my_base_url = "https://api.passtools.com/v1"):
        """
        Init new pt_service.Service instance

        @type my_api_key: str
        @param my_api_key: User-specific API key required for accessing PassTools API
        @return: None
        """
        super(Service, self).__init__()
        # Share the api_key and base_url with all importers of the module
        global api_key
        api_key = my_api_key.encode('utf8')
        global base_url
        base_url = my_base_url
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

    def delete_template(self, template_id = None):
        """
        Delete Template specified by template_id

        API call used is v1/template (DELETE)

        @type template_id: int
        @param template_id: ID of the template to delete
        @return: None
        """
        temp_template = Template()
        temp_template.delete(template_id)

    def count_templates(self):
        """
        Retrieve count of existing templates created by owner of API-key

        API call used is v1/template (GET)

        @return: Integer
        """
        temp_template = Template()
        return temp_template.count()

    def list_templates(self, **kwargs):
        """
        Retrieve list of existing templates created by owner of API-key
        Optional parameters are translated into query-modifiers

        Note that list() returns abbreviated form of templates. Use get() to retrieve full template.

        API call used is v1/template/headers (GET)

        @type pageSize: int
        @param pageSize: Maximum length of list to return [Optional; Default = 10]
        @type page: int
        @param page: 1-based index of page into list, based on page_size [Optional; Default = 1]
        @type order: string
        @param order: Name of field on which to sort list [Optional; From (ID, Name, Created, Updated)]
        @type direction: string
        @param direction: Direction which to sort list [Optional; From (ASC, DESC)]
        @return: List of pt_template.Template instances
        """
        temp_template = Template()
        return temp_template.list(**kwargs)

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

    def update_pass(self, pass_id, update_fields = None):
        """
        Update existing pass

        API call used is v1/pass/<pass_id> (PUT)

        @type pass_id: int
        @param pass_id: ID of pt_pass.Pass to update
        @type update_fields: dict
        @param update_fields: template_fields_model dict of the template used to create new pass
        @return: pt_pass.Pass instance
        """
        temp_pass = Pass()
        new_pass = temp_pass.get(pass_id)
        return new_pass.update(update_fields)

    def push_pass(self, target_pass_id):
        """
        Push update to existing pass

        API call used is v1/pass/<pass_id>/push (PUT)

        @type pass_id: int
        @param pass_id: ID of pt_pass.Pass to update
        @return: Dict
        """
        temp_pass = Pass()
        new_pass = temp_pass.get(target_pass_id)
        return new_pass.push()

    def get_pass(self, pass_id = None):
        """
        Retrieve existing pass with specified ID

        API call used is v1/pass/<pass_id> (GET)

        @type pass_id: int
        @param pass_id: ID of desired pt_pass.Pass.
        @return: pt_pass.Pass instance
        """
        temp_pass = Pass()
        new_pass = temp_pass.get(pass_id)

        return new_pass

    def delete_pass(self, pass_id = None):
        """
        Delete existing pass with specified ID

        API call used is v1/pass/<pass_id> (DELETE)

        @type pass_id: int
        @param pass_id: ID of pt_pass.Pass to delete
        @return: None
        """
        temp_pass = Pass()
        temp_pass.delete(pass_id)

    def count_passes(self, template_id = None):
        """
        Retrieve count of existing passes created by owner of API-key
        If template_id is specified, count only passes associated with that template
        Other parameters are translated into query-modifiers

        API call used is v1/pass (GET)

        @type templateId: int
        @param templateId: ID of the template used to create new pass
        @return: Integer
        """
        temp_pass = Pass()
        return temp_pass.count(template_id)

    def list_passes(self, **kwargs):
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
        @param direction: Direction which to sort list [Optional; From (ASC, DESC)]
        @return: List of pt_pass.Pass instances
        """
        temp_pass = Pass()
        return temp_pass.list(**kwargs)

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
