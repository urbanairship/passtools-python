##########################################
# 
# Define PassTools API package
#
# Copyright 2013, Urban Airship, Inc.
##########################################
"""
Python SDK for PassTools API

Provides simple Python-based interface to the PassTools API, which allows user to create, retrieve, update, and download
PassTools passes.


"""

from pt_client import PassToolsClient

class PassTools(object):

    api_version = "1.0.3"
    api_key = None
    base_url = "https://api.passtools.com/v1"
    request_client = None

    @classmethod
    def configure(cls, api_key = None, base_url = "https://api.passtools.com/v1"):
        cls.api_key = api_key
        cls.base_url = base_url
        cls.request_client = PassToolsClient(cls.api_key, cls.base_url)

    @classmethod
    def check_service(cls):
        request_url = "/system/status"
        response_code, response_data = cls.request_client.pt_get_json(request_url)
        return response_code == 200
