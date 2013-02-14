#!/usr/bin/env python
##########################################
# pt_client.py
# 
# Interface to PassTools REST API
#
# Copyright 2013, Urban Airship, Inc.
##########################################
"""
HTTP interface to PassTools REST API, used indirectly, via other PassTools classes.

"""

import copy
import requests

try:
    import simplejson as json
except ImportError:
    import json

from passtools import PassTools

SSL_CERT_VERIFY = False
STD_ENCODING = "ISO-8859-1"
STD_HEADERS = {'Content-Type':'application/x-www-form-urlencoded', 'Accept':'*/*'}

def __pt_request(request_func, request_url_frag, request_data = {}):
    """
    Base HTTP request handler. Called only indirectly.

    @type request_func: function
    @param request_func: Function requested
    @type request_url_frag: str
    @param request_url_frag: URL fragment (to be appended to base_URL)
    @type request_data: dict
    @param request_data: Request parameters
    @return: json form of template full-form description
    """
    if not PassTools.api_key:
        raise RuntimeError("No API secret key provided. Cannot continue.")
    request_url = "%s%s" % (PassTools.base_url, request_url_frag)

    request_data_dict = copy.deepcopy(request_data)
    request_data_dict.update({"api_key":PassTools.api_key})

    resp = request_func(request_url, params = request_data_dict, headers = STD_HEADERS, verify = SSL_CERT_VERIFY)
    __raise_for_status(resp)

    resp.encoding = STD_ENCODING
    # User can request raw response by setting test_mode = True; else returns will be json-decoded
    # And hate to special case like this, but download needs special handling
    if PassTools.test_mode or ('download' in request_url):
        return resp
    else:
        return resp.json()

def pt_get(request_url_frag, request_data = {}):
    """
    HTTP GET

    @type request_func: function
    @param request_func: Function requested
    @type request_url_frag: str
    @param request_url_frag: URL fragment (to be appended to base_URL)
    @type request_data: dict
    @param request_data: Request parameters
    @return: json form of template full-form description
    """
    return __pt_request(requests.get, request_url_frag, request_data)

def pt_post(request_url_frag, request_data = {}):
    """
    HTTP POST

    @type request_func: function
    @param request_func: Function requested
    @type request_url_frag: str
    @param request_url_frag: URL fragment (to be appended to base_URL)
    @type request_data: dict
    @param request_data: Request parameters
    @return: json form of template full-form description
    """
    return __pt_request(requests.post, request_url_frag, request_data)

def pt_put(request_url_frag, request_data = {}):
    """
    HTTP PUT

    @type request_func: function
    @param request_func: Function requested
    @type request_url_frag: str
    @param request_url_frag: URL fragment (to be appended to base_URL)
    @type request_data: dict
    @param request_data: Request parameters
    @return: json form of template full-form description
    """
    return __pt_request(requests.put, request_url_frag, request_data)

def pt_delete(request_url_frag, request_data = {}):
    """
    HTTP DELETE

    @type request_func: function
    @param request_func: Function requested
    @type request_url_frag: str
    @param request_url_frag: URL fragment (to be appended to base_URL)
    @type request_data: dict
    @param request_data: Request parameters
    @return: json form of template full-form description
    """
    return __pt_request(requests.delete, request_url_frag, request_data)


def __raise_for_status(response):
    # Override the version in Requests so I can get better reporting

    http_error_msg = ''

    if 400 <= response.status_code < 500:

        decoded_content = ""
        content_dict = json.loads(response.content, encoding='ISO-8859-1')
        if "description" in content_dict:
            decoded_content += content_dict['description'] + " "
        if "details" in content_dict:
            decoded_content += content_dict['details']
        http_error_msg = '%s Client Error: %s. %s' % (response.status_code, response.reason, decoded_content)

    elif 500 <= response.status_code < 600:
        http_error_msg = '%s Server Error: %s' % (response.status_code, response.reason)

    if http_error_msg:
        http_error = PassToolsException(http_status=response.status_code, message=http_error_msg, response=response)
        http_error.response = response
        raise http_error


class PassToolsException(Exception):
    def __init__(self, http_status=None, message=None, response=None):
        super(PassToolsException, self).__init__(message)
