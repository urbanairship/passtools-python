import copy
import sys
import time
from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template
from passtools.pt_tag import Tag

# API User:
# STEP 1: Retrieve your API key from your Account view on the PassTools website
my_api_key = "your-key-goes-in-here"
my_api_key = "test"
my_base_url="http://localhost:8080/v1"

# STEP 2:
# You'll always configure the api, providing your api key.
# This is required!
PassTools.configure(api_key = my_api_key, base_url = my_base_url)
