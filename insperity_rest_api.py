"""
Functions for calling the Insperity REST API endpoints

https://insperity.myisolved.com/rest

To call the REST API, first get the access token, client ID, and legal ID:

    load_dotenv()  # load environment variables from .env file, such as client_code and secret
    access_token = get_client_credential_token(client_code=LEGAL_ID_VES)
    client_id, legal_ids = get_client_and_legal_ids(access_token)

Then can get legal ID for a particular "company":

    legal_id, legal_links = get_legal_id(legal_ids, 'Newport')

Then can use these to call API endpoints:

    response = get_employee_list(token_dict, client_id, legal_id, minimal=True)
    print(f"number of employees returned: {len(response)}")

Len Wanger
2025
"""

from insperity_rest_utils import *

BASE_URL = "https://insperity.myisolved.com/rest/api"
GET_TOKEN = f"{BASE_URL}/token"  # POST
CLIENTS = f"{BASE_URL}/clients"  # "https://insperity.myisolved.com/rest/api/clients"
LEGALS = f"{BASE_URL}/legals"  # "https://insperity.myisolved.com/rest/api/legals"
EMPLOYEES_MIN = "https://insperity.myisolved.com/rest/api/clients/{client_id}/legals/{legal_id}/employeesMinimal"
EMPLOYEES = "https://insperity.myisolved.com/rest/api/clients/{client_id}/employees"


##############################################################################################################
# Refresh token decorator -- used to wrap endpoint functions that call the REST API. Will call to refresh the
#   refresh token if access token expires, otherwise will just return the response from the endpoint function
#   or raise an exception if the status code is not 200.
##############################################################################################################
def refresh_token(f):
   @wraps(f)
   def wrapper(token_dict, *args, **kwds):
       retries = 0

       while True:
           response = f(token_dict, *args, **kwds)

           if response.status_code == 200:
               break
           elif (retries < 1) and (response.status_code == 401):  # get refresh token and try again
               new_token_dict = get_refresh_token(token_dict=token_dict)
               token_dict['refresh_token'] = new_token_dict['refresh_token']
               token_dict['access_token'] = new_token_dict['access_token']
               retries += 1
           else:
               raise requests.exceptions.HTTPError(
                   f"Error call {f.__name__} (status={response.status_code}): {response.text}")

       response_dict = json.loads(response.content)
       return response_dict['results']

   return wrapper


##############################################################################################################
# REST API endpoint functions
##############################################################################################################
def get_client_credential_token(client_code: str) -> dict:
    """
    Get access token using client_credentials grant type.

    :param client_code: Insperity customer/client code
    :return: dictionary containing access_token and refresh_token
    """
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

    return {
        'access_token': response_dict['access_token'], 
        'refresh_token': response_dict['refresh_token'],
        'client_code': client_code
    }


def get_refresh_token(token_dict: dict) -> dict:
    """
    Get refresh token using refresh_token grant type.
    
    :param token_dict:
    :return: dictionary containing access_token and refresh_token
    """
    combined_key = get_combined_key()

    headers = {
        "Authorization": f"Basic {combined_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": token_dict['refresh_token'],
        "clientCode": token_dict['client_code']
    }

    response = requests.post(GET_TOKEN, headers=headers, data=payload)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(
            f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)

    return {
        'access_token': response_dict['access_token'], 
        'refresh_token': response_dict['refresh_token'],
        'client_code': token_dict['client_code']
    }


@refresh_token
def get_client_info(token_dict: dict) -> dict:
    # test getting client information
    headers = get_headers(token_dict['access_token'])
    response = requests.get(CLIENTS, headers=headers)
    return response


@refresh_token
def get_client_id(token_dict: dict) -> str:
    # test getting client information
    headers = get_headers(token_dict['access_token'])
    response = requests.get(CLIENTS, headers=headers)
    return response


def get_legals(token_dict: dict) -> dict:
    # test getting client information
    headers = get_headers(token_dict['access_token'])
    response = requests.get(LEGALS, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Error getting client information (status={response.status_code}): {response.text}")

    response_dict = json.loads(response.content)
    return response_dict['results']


def get_client_and_legal_ids(token_dict: dict) -> tuple[str, dict]:
    # test getting client information
    headers = get_headers(token_dict['access_token'])
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


def get_employee_list(token_dict: dict, client_id: str, legal_id: str, minimal=True) -> list[dict]:
    # return a list of dicts of employee information (minimal employee info if minimal=True, full employee info if minimal=False)
    employee_list = []
    headers = get_headers(token_dict['access_token'])

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