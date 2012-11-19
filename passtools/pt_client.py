#!/usr/bin/env python
##########################################
# pt_client.py
# 
# Interface to PassTools REST API
#
# Copyright 2012, Tello, Inc.
##########################################
"""
HTTP interface to PassTools REST API, used indirectly, via other PassTools classes.

"""

try:
    import simplejson as json
except ImportError:
    import json

import copy
import logging
import urllib
import urllib2

from pt_exceptions import *
import pt_service

the_logger = logging.getLogger('')

#########################
# CLASS PassToolsClient
# 
#
#########################
class PassToolsClient(object):

    def __api_key_check(self):
        if not pt_service.api_key:
            raise AuthenticationException("No API secret key provided. Did you create a pt_service instance?")

    def __dispatch_exception(self, response_code, fail_msg, request):
        if response_code == 200:
            return
        request_url = request._Request__original
        get_params = request_url.split("?")
        post_params = request.headers
        if len(get_params) > 1:
            params = get_params[1:]
        elif post_params != {}:
            params = post_params
        else:
            params = ""
        if response_code < 400:
            raise PassToolsException(message = fail_msg, http_status = response_code)
        elif response_code == 400:
            raise InvalidRequestException(message = fail_msg, param=params, http_status = response_code)
        elif response_code == 401:
            raise AuthenticationException(message = fail_msg, http_status = response_code)
        elif response_code == 406:
            raise InvalidRequestException(message = fail_msg, param=params, http_status = response_code)
        elif response_code == 429:
            raise TooManyRequestsException(message = fail_msg, http_status = response_code)
        elif response_code >= 500:
            raise InternalServerException(message = fail_msg, http_status = response_code)
        else:
            raise APIException()

    def __run_request(self, request):
        response_code = None
        response_data = {}
        try:
            # Open the request on the url
            http_verbosity = 0     # For debugging purposes...turn it up to 10
            opener = urllib2.build_opener(urllib2.HTTPHandler(http_verbosity))
            request_handle = opener.open(request)

            # Get the data from the response
            response_code = request_handle.code
            response_data = request_handle.read()
            request_handle.close()
            the_logger.debug("Response code: %d" % response_code)

        except urllib2.URLError, e:
            fail_msg = "Error"
            # If exception includes no status code but a reason, it's a URLError
            if hasattr(e, 'reason'):
                response_code = e.reason.errno
                fail_msg = "Communication with host '%s' failed: %s (errno %s)" % (request.host, e.reason.strerror, response_code)
             # else if exception includes an HTTP status code, it's an HTTPError
            elif hasattr(e, 'code'):
                response_code = e.code
                fail_msg = "HTTPError (%s)" % response_code
                if response_code < 500:
                # If not a server error, read error details from the returned page
                    try:
                        err_page_dict = json.load(e)
                        if 'description' in err_page_dict:
                            fail_msg += (" %s" % err_page_dict['description'])
                        if 'details' in err_page_dict:
                            if err_page_dict['details'] == "field errors" and "fieldErrors" in err_page_dict:
                                fail_msg += " Details:\n"
                                for err_item in err_page_dict['fieldErrors']:
                                    fail_msg += err_item["message"] + "\n"
                            else:
                                fail_msg += (" Details: '%s'" % err_page_dict['details'])
                    except:
                        raise
                else:
                # For a server error, don't count on an error page
                     if hasattr(e, 'msg'):
                        fail_msg += (": %s" % e.msg)

            the_logger.error(fail_msg)

            self.__dispatch_exception(response_code, fail_msg, request)

        return response_code, response_data

    def pt_get_json(self, request_url_frag, request_data_dict = {}):
        """
        Make an HTTP GET request of specified URL

        @type request_url_frag: str
        @param request_url_frag: target URL (base_url will be prepended)
        @type request_data_dict: dict
        @param request_data_dict: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s?api_key=%s" % (pt_service.base_url, request_url_frag, pt_service.api_key)

        # Append any request data
        for keyName in request_data_dict:
            request_url += "&" + keyName + "=" + str(request_data_dict[keyName])

        # create request
        req = urllib2.Request(request_url)
        the_logger.debug("pt_get request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)
        if response_code == 200:
            the_logger.debug("pt_get response:\n%s" % (response_data))

        return response_code, response_data

    def pt_get_dict(self, request_url, request_data_dict = {}):
        """
        Make an HTTP GET request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type request_data_dict: dict
        @param request_data_dict: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.pt_get_json(request_url, request_data_dict)
        if response_code == 200:
            response_data_dict = json.loads(response_data, encoding="ISO-8859-1")
        return response_code, response_data_dict

    def pt_post_json(self, request_url_frag, request_data):
        """
        Make an HTTP POST request of specified URL

        @type request_url_frag: str
        @param request_url_frag: target URL (base_url will be prepended)
        @type request_data: dict
        @param request_data: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s" % (pt_service.base_url, request_url_frag)

        request_data_dict = copy.deepcopy(request_data)
        # Append api_key to request
        self.__api_key_check()
        request_data_dict["api_key"] = pt_service.api_key

        # Format the input data
        encoded_request_data = urllib.urlencode(request_data_dict)
        the_logger.debug("encoded request_data: %s" % encoded_request_data)

        # Prepare headers
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = '*/*'

        # create a request
        req = urllib2.Request(request_url, encoded_request_data, headers=headers)
        the_logger.debug("pt_post request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)
        if response_code == 200:
            the_logger.debug("pt_post response:\n%s" % (response_data))

        return response_code, response_data

    def pt_post_dict(self, request_url, request_data):
        """
        Make an HTTP POST request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type request_data: dict
        @param request_data: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.pt_post_json(request_url, request_data)
        if response_code == 200:
            response_data_dict = json.loads(response_data, encoding="ISO-8859-1")
        return response_code, response_data_dict

    def pt_put(self, request_url_frag, request_data = {}):
        """
        Make an HTTP PUT request of specified URL

        @type request_url_frag: str
        @param request_url_frag: target URL (base_url will be prepended)
        @type request_data: dict
        @param request_data: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s" % (pt_service.base_url, request_url_frag)


        request_data_dict = copy.deepcopy(request_data)
        # Append api_key to request
        self.__api_key_check()
        request_data_dict["api_key"] = pt_service.api_key

        # Format the input data
        encoded_request_data = urllib.urlencode(request_data_dict)
        the_logger.debug("encoded request_data: %s" % encoded_request_data)

        # Prepare headers
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = '*/*'

        # create a request
        req = urllib2.Request(request_url, encoded_request_data, headers=headers)
        req.get_method = lambda: 'PUT'
        the_logger.debug("pt_put request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)

        return response_code, response_data

    def pt_put_json(self, request_url, request_data = {}):
        """
        Make an HTTP PUT request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type request_data: dict
        @param request_data: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.pt_put(request_url, request_data)
        if response_code == 200:
            response_data_json = json.loads(response_data, encoding="ISO-8859-1")
            the_logger.debug("pt_put response:\n%s" %
                             json.dumps(response_data, sort_keys = True, indent = 2))
        return response_code, response_data_json

    def pt_delete(self, request_url_frag, request_data_dict):
        """
        Make an HTTP DELETE request of specified URL

        @type request_url_frag: str
        @param request_url_frag: target URL (base_url will be prepended)
        @type request_data: dict
        @param request_data: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s?api_key=%s" % (pt_service.base_url, request_url_frag, pt_service.api_key)

        # Append any request data
        for keyName in request_data_dict:
            request_url += "&" + keyName + "=" + str(request_data_dict[keyName])

        # Prepare headers
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = '*/*'

        # create a request
        req = urllib2.Request(request_url)
        req.get_method = lambda: 'DELETE'
        the_logger.debug("pt_put request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)

        return response_code, response_data

    def pt_delete_json(self, request_url, request_data):
        """
        Make an HTTP DELETE request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type request_data: dict
        @param request_data: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.pt_delete(request_url, request_data)
        if response_code == 200:
            response_data_json = json.loads(response_data, encoding="ISO-8859-1")
            the_logger.debug("pt_delete response:\n%s" %
                             json.dumps(response_data, sort_keys = True, indent = 2))
        return response_code, response_data_json

