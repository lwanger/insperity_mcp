"""
Utility functions used by Insperity REST API

https://insperity.myisolved.com/rest

Len Wanger
2025
"""

import base64
from functools import wraps
import json
import os

import requests


# ##############################################################################################################
# # Refresh token decorator -- used to wrap endpoint functions that call the REST API. Will call to refresh the
# #   refresh token if access token expires, otherwise will just return the response from the endpoint function
# #   or raise an exception if the status code is not 200.
# ##############################################################################################################
# def refresh_token(f):
#    @wraps(f)
#    def wrapper(token_dict, *args, **kwds):
#        retries = 0
#
#        while True:
#            response = f(token_dict, *args, **kwds)
#
#            if response.status_code == 200:
#                break
#            elif (retries < 1) and (response.status_code == 401):  # get refresh token and try again
#                # new_token_dict = get_refresh_token(client_code=client_code, token_dict=token_dict)
#                new_token_dict = get_refresh_token(token_dict=token_dict)
#                token_dict['refresh_token'] = new_token_dict['refresh_token']
#                token_dict['access_token'] = new_token_dict['access_token']
#                retries += 1
#            else:
#                raise requests.exceptions.HTTPError(
#                    f"Error call {f.__name__} (status={response.status_code}): {response.text}")
#
#        response_dict = json.loads(response.content)
#        return response_dict['results']
#
#    return wrapper


##############################################################################################################
# Utility routines used by endpoints
##############################################################################################################
def to_mime_base64(input_string: str) -> str:
    # Convert a string to RFC2045-MIME variant of Base64.
    byte_data = input_string.encode("utf-8")
    mime_encoded = base64.b64encode(byte_data)
    return mime_encoded.decode("utf-8")


def get_combined_key() -> str:
    # create combined key used in header for REST API calls
    return to_mime_base64(f"{os.getenv('INSPERITY_CLIENT_ID')}:{os.getenv('INSPERITY_SECRET')}")


def get_headers(access_token: str) -> dict:
    # create header dictionary used by requests for REST API calls
    return {
        'Authorization': f"Bearer {access_token}",
        'essScope': "Employee"  # ?essScope={Employee|Manager|Supervisor|All*}
    }