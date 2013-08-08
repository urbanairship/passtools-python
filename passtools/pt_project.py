import json
import urllib
import pt_client

class Project:
    def __init__(self):
        """

        @return:
        """

    @classmethod
    def list(cls, **kwargs):
        """

        @param cls:
        @return:
        """
        request_dict = kwargs
        request_url = "/project"
        return pt_client.pt_get(request_url, request_dict)


    @classmethod
    def create(cls, project_dict, external_id=None):
        """

        @param cls:
        @param project_dict:
        @param external_id:
        @return:
        """
        request_url = "/project"
        if external_id is not None:
            request_url = "/project/id/%s" % urllib.quote_plus(external_id)

        request_dict = {"json": json.dumps(project_dict, encoding="ISO-8859-1")}
        return pt_client.pt_post(request_url, request_dict)


    @classmethod
    def get(cls, project_id):
        """

        @param cls:
        @param project_id:
        @return:
        """
        request_url = "project/%d" % int(project_id)
        return pt_client.pt_get(request_url)

    @classmethod
    def get_by_external_id(cls, external_id):
        """

        @param cls:
        @param project_external_id:
        @return:
        """
        request_url = "project/id/%s" % urllib.quote_plus(external_id)
        return pt_client.pt_get(request_url)

    @classmethod
    def update(cls, project_id, project_dict):
        """

        @param cls:
        @param project_id:
        @param project_dict:
        @return:
        """
        request_url = "project/%d" % int(project_id)
        request_dict = {"json": json.dumps(project_dict, encoding="ISO-8859-1")}
        return pt_client.pt_put(request_url, request_dict)

    @classmethod
    def update_by_external_id(cls, external_id, project_dict):
        """

        @param cls:
        @param external_id:
        @param project_dict:
        @return:
        """
        request_url = "project/id/%s" % urllib.quote_plus(external_id)
        request_dict = {"json": json.dumps(project_dict, encoding="ISO-8859-1")}
        return pt_client.pt_put(request_url, request_dict)

    @classmethod
    def delete(cls, project_id):
        """

        @param cls:
        @param project_id:
        @return:
        """

        request_url = "project/%d" % int(project_id)
        return pt_client.pt_delete(request_url)

    @classmethod
    def delete_by_external_id(cls, external_id):
        """

        @param cls:
        @param external_id:
        @return:
        """

        request_url = "project/id/%s" % urllib.quote_plus(external_id)
        return pt_client.pt_delete(request_url)



