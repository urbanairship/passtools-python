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

class PassTools(object):

    api_version = "1.0.4"
    api_key = None
    base_url = None
    request_client = None
    test_mode = False

    @classmethod
    def configure(cls, api_key = None, base_url = "https://api.passtools.com/v1"):
        cls.api_key = api_key
        cls.base_url = base_url

    @classmethod
    def check_service(cls):
        request_url = "/system/status"
        response_code, response_data = cls.request_client.pt_get_json(request_url)
        return response_code == 200
