"""
Utility functions used by Insperity REST API

https://insperity.myisolved.com/rest

Len Wanger
2025
"""

import base64
import os


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