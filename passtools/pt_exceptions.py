##########################################
# pt_exceptions.py
# 
# Exceptions raised by PassTools Client
#
# Copyright 2012, Tello, Inc.
##########################################
"""
Collected exception classes for PassTools SDK

"""


class PassToolsException(Exception):
  def __init__(self, message=None, http_body=None, http_status=None, json_body=None):
    super(PassToolsException, self).__init__(message)
    self.http_body = http_body
    self.http_status = http_status
    self.json_body = json_body

class APIException(PassToolsException):
  pass

class AuthenticationException(PassToolsException):
  pass

class InternalServerException(PassToolsException):
  pass

class InvalidParameterException(PassToolsException):
  pass

class TooManyRequestsException(PassToolsException):
    pass

class InvalidRequestException(PassToolsException):
  def __init__(self, message, param, http_body=None, http_status=None, json_body=None):
    super(InvalidRequestException, self).__init__(message, http_body, http_status, json_body)
    self.param = param


