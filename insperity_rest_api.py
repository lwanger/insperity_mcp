"""
Utitily functions for calling the Insperity REST API

https://insperity.myisolved.com/rest

To call the REST API, first get the access token, client ID, and legal ID:

    load_dotenv()  # load environment variables from .env file, such as client_code and secret
    access_token = get_client_credential_token(client_code=LEGAL_ID_VES)
    client_id, legal_ids = get_client_and_legal_ids(access_token)

Then can get legal ID for a particular "company":

    legal_id, legal_links = get_legal_id(legal_ids, 'Newport')

Then can use these to call API endpoints:

    response = get_employee_list(access_token, client_id, legal_id, minimal=True)
    print(f"number of employees returned: {len(response)}")

Len Wanger
2025
"""

import base64
import json
import os

import requests


BASE_URL = "https://insperity.myisolved.com/rest/api"
GET_TOKEN = f"{BASE_URL}/token"  # POST
CLIENTS = f"{BASE_URL}/clients"  # "https://insperity.myisolved.com/rest/api/clients"
LEGALS = f"{BASE_URL}/legals"  # "https://insperity.myisolved.com/rest/api/legals"
EMPLOYEES_MIN = "https://insperity.myisolved.com/rest/api/clients/{client_id}/legals/{legal_id}/employeesMinimal"
# EMPLOYEES = "https://insperity.myisolved.com/rest/api/clients/{client_id}/legals/{legal_id}/employees"
EMPLOYEES = "https://insperity.myisolved.com/rest/api/clients/{client_id}/employees"


def to_mime_base64(input_string: str) -> str:
    """
    Convert a string to RFC2045-MIME variant of Base64.
    """
    byte_data = input_string.encode("utf-8")
    mime_encoded = base64.b64encode(byte_data)
    return mime_encoded.decode("utf-8")


def get_combined_key() -> str:
    return to_mime_base64(f"{os.getenv('INSPERITY_CLIENT_ID')}:{os.getenv('INSPERITY_SECRET')}")


def get_headers(access_token: str) -> dict:
    return {
        'Authorization': f"Bearer {access_token}",
        'essScope': "Employee"  # ?essScope={Employee|Manager|Supervisor|All*}
    }


def get_client_credential_token(client_code: str) -> str:
    # get access token using client_credentials
    combined_key = get_combined_key()

    headers = {
        "Authorization": f"Basic {combined_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "client_credentials",
        "clientCode": client_code,
    }

    response = requests.post(GET_TOKEN, headers=headers, data=payload)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    # print(f"{response.status_code=}: {response.text=}")
    return response_dict['access_token']


def get_client_info(access_token: str) -> dict:
    # test getting client information
    headers = get_headers(access_token)
    response = requests.get(CLIENTS, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    return response_dict['results']


def get_client_id(access_token: str) -> str:
    # test getting client information
    headers = get_headers(access_token)
    response = requests.get(CLIENTS, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    return response_dict['results'][0]['id']


def get_legals(access_token: str) -> dict:
    # test getting client information
    headers = get_headers(access_token)
    response = requests.get(LEGALS, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    return response_dict['results']


def get_client_and_legal_ids(access_token: str) -> tuple[str, dict]:
    # test getting client information
    headers = get_headers(access_token)
    response = requests.get(CLIENTS, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    client_id = response_dict['results'][0]['id']

    response = requests.get(LEGALS, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    legal_ids = response_dict['results']
    return client_id, legal_ids


def get_legal_id(legal_ids: dict, legal_name_substring: str) -> tuple[str, dict]:
    # return the first legal id that matches the name substring
    for legal_id in legal_ids:
        if legal_name_substring in legal_id['legalName']:
            return legal_id['id'], legal_id['links']

    return None


# def call_legal_link(access_token: str, legal_links: dict, endpoint: str) -> dict:
#     """
#     call from dict of legal links. Endpoints are:
#         self (legals)
#         parent
#         Employees
#         Detailed
#         Timeclocks
#         MiscFields
#     """
#     headers = get_headers(access_token)
#
#     for legal_link in legal_links:
#         if legal_link['rel'] == endpoint:
#             response = requests.get(legal_link['href'], headers=headers)
#
#             if response.status_code != 200:
#                 raise requests.exceptions.HTTPError(
#                     f"Error getting client information (status={response.status_code}): {response.text}")
#
#             response_dict = json.loads(response.content)
#             return response_dict
#
#         raise ValueError(f"Endpoint {endpoint} not found in legal links")


def get_employee_list(access_token: str, client_id: str, legal_id: str, minimal=True) -> list[dict]:
    # return a list of dicts of employee information (minimal employee info if minimal=True, full employee info if minimal=False)
    employee_list = []
    headers = get_headers(access_token)

    if minimal is True:
        url = EMPLOYEES_MIN.format(client_id=client_id, legal_id=legal_id)
    else:
        url = EMPLOYEES.format(client_id=client_id, legal_id=legal_id)

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Error getting minimal employee information (status={response.status_code}): {response.text}")

        response_dict = json.loads(response.content)
        employee_list += response_dict['results']

        if response_dict['nextPageUrl'] is None:
            break

        url = response_dict['nextPageUrl']

    return employee_list