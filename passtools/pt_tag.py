try:
    import simplejson as json
except ImportError:
    import json

import urllib
from urllib import quote_plus
import pt_client
from passtools import PassTools

class Tag:
    def __init__(self, tag):
        """
        @param tag:
        @return:
        """
        self.__tag = tag

    @staticmethod
    def list(**kwargs):
        """
        Retrieve list of tags for owner of API-key
        Optional parameters are translated into query-modifiers

        API call used is v1/tag (GET)

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
        request_url = "/tag"
        return pt_client.pt_get(request_url, request_dict)

    @classmethod
    def get_passes(cls, tag, **kwargs):
        """
        Retrieve list of pass for the tag
        Optional parameters are translated into query-modifiers

        API call used is v1/tag (GET)

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
        request_url = "/tag/%s/passes" % urllib.quote_plus(tag);
        return pt_client.pt_get(request_url, request_dict)


    @classmethod
    def update_passes(cls, tag, fields_model_dict):
        """

        @param cls:
        @param fields_model_dict:
        @return:
        """
        request_url = "/tag/%s/passes" % urllib.quote_plus(tag)
        request_dict = {"json": json.dumps(fields_model_dict, encoding="ISO-8859-1")}
        return pt_client.pt_put(request_url, request_dict)


    @classmethod
    def delete_tag(cls, tag):
        """

        @param cls:
        @param tag:
        @return:
        """

        request_url = "/tag/%s" % urllib.quote_plus(tag)
        return pt_client.pt_delete(request_url)



    @classmethod
    def removeTagFromPasses(cls, tag):
        """

        @param cls:
        @param tag:
        @return:
        """

        request_url = "tag/%s/passes" % urllib.quote_plus(tag)
        return pt_client.pt_delete(request_url)

    @classmethod
    def removeTagFromPass(cls, tag, pass_id):
        """

        @param cls:
        @param tag:
        @return:
        """

        request_url = "tag/%s/pass/%d" % (urllib.quote_plus(tag), int(pass_id))
        return pt_client.pt_delete(request_url)

    @classmethod
    def removeTagFromPassX(cls, tag, pass_external_id):
        """

        @param cls:
        @param tag:
        @param pass_external_id:
        @return:
        """
        request_url = "tag/%s/pass/id/%d" % (urllib.quote_plus(tag), pass_external_id)
        return pt_client.pt_delete(request_url)