"""
Test Insperity REST API

URL: https://myisolved.com/rest

Note that your production calls will be to insperity.myisolved.com
legal id 2502007-1,2,3 (ves, npt, lv)

Here is the information you need for immediate access to the API Specifications:

URL: https://myisolved.com/rest

Sample endpoints on the call:

To get your client ID and legal company ID that will be referenced in other endpoints:
List of Clients - https://insperity.myisolved.com/rest/api/clients
List of Legal Companies - https://insperity.myisolved.com/rest/api/legals


To get the employee IDs that will be referenced in the other endpoints:
Get Minimal Employee List – returns the employee ID, name, email, and a few other basic employee details - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employeesMinimal
Get Employees by Client – returns lots of employee demographic details (if you need it) - https://insperity.myisolved.com/rest/api/clients/{clientId}/employees


To get the time card punches to track in / out status
Get time card data (there is a version where you can pass a date parameter too) - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/timecardView
Use the timecardHourResults dataset to get information after the time rules are applied
Alerts in the timecardVerifications dataset can include an approaching overtime alert if we build that in your system
Employee Dashboard - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/dashboard/filterOptions

TODO:
    - implement request of access token
    - handle paginated results
"""

import base64
import json
import os

from dotenv import load_dotenv
import requests

LEGAL_ID_VES = '2502007-1'
LEGAL_ID_NPT = '2502007-2'
LEGAL_ID_LV = '2502007-3'

BASE_URL = "https://insperity.myisolved.com/rest/api"
# GET_TOKEN = "https://insperity.myisolved.com/rest/api/token"  # POST
GET_TOKEN = f"{BASE_URL}/token"  # POST
CLIENTS = f"{BASE_URL}/clients"  # "https://insperity.myisolved.com/rest/api/clients"
LEGALS = f"{BASE_URL}/legals"  # "https://insperity.myisolved.com/rest/api/legals"
EMPLOYEE = "" # https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employeesMinimal


def to_mime_base64(input_string: str) -> str:
    """
    Convert a string to RFC2045-MIME variant of Base64.
    """
    # Encode string to bytes
    byte_data = input_string.encode("utf-8")
    mime_encoded = base64.b64encode(byte_data)
    return mime_encoded.decode("utf-8")

def get_combined_key() -> str:
    # client_id = os.getenv('INSPERITY_CLIENT_ID')
    # secret = os.getenv('INSPERITY_SECRET')
    # user = os.getenv('INSPERITY_USER')
    # pwd = os.getenv('INSPERITY_PWD')
    combined_key = to_mime_base64(f"{os.getenv('INSPERITY_CLIENT_ID')}:{os.getenv('INSPERITY_SECRET')}")

    return combined_key


def get_client_password_token() -> str:
    # MFA is not working.... URL can't be found
    # get access token
    combined_key = get_combined_key()

    headers = {
        "Authorization": f"Basic {combined_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "password",
        "username": os.getenv('INSPERITY_USER'),
        "password": os.getenv('INSPERITY_PWD'),
        "clientCode": LEGAL_ID_VES,
    }

    response = requests.post(GET_TOKEN, headers=headers, data=payload)

    # should be 403 (needs MFA) -- reason="mfa_required"
    response_dict = json.loads(response.content)
    mfa_token = response_dict['mfaToken']
    payload['mfa_token'] = mfa_token

    # get auth code from SMS
    idx = response_dict['mfaSMSRoute'].find('?')
    queries = response_dict['mfaSMSRoute'][idx+1:].split('&')

    # idx = response_dict['mfaEmailRoute'].find('?')
    # queries = response_dict['mfaEmailRoute'][idx + 1:].split('&')

    headers2 = {}
    for query in queries:
        if len(query) > 0:
            key, value = query.split('=')
            headers2[key] = value

    response = requests.post(url=response_dict['mfaSMSRoute'][:idx], headers=headers)
    # response = requests.post(url=response_dict['mfaEmailRoute'][:idx], headers=headers2)

    mfa_auth_code = input("Enter MFA code: ")
    payload['mfa_code'] = mfa_auth_code

    response = requests.post(GET_TOKEN, headers=headers, data=payload)

    print(f"{response.status_code=}: {response.text=}")
    return response_dict['access_token']


def get_client_credential_token() -> str:
    # get access token using client_credentials
    combined_key = get_combined_key()

    headers = {
        "Authorization": f"Basic {combined_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "client_credentials",
        "clientCode": LEGAL_ID_VES,
    }

    response = requests.post(GET_TOKEN, headers=headers, data=payload)
    response_dict = json.loads(response.content)
    # print(f"{response.status_code=}: {response.text=}")
    return response_dict['access_token']


def get_client_info(access_token: str) -> dict:
    headers = {}
    headers['Authorization'] = f"Bearer {access_token}"
    headers['essScope'] = "Employee"  # ?essScope={Employee|Manager|Supervisor|All*}

    # test getting client information
    response = requests.get(CLIENTS, headers=headers)
    response_dict = json.loads(response.content)
    results = response_dict['results']
    return results


if __name__ == '__main__':
    load_dotenv()
    access_token = get_client_credential_token()

    # test using the token
    results = get_client_info(access_token)
    print(f"{results[0]['clientCode']=}: {results[0]['clientName']=}")






