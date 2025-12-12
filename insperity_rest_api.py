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

    response = get_employee_list(token_dict, client_id, legal_id)
    print(f"number of employees returned: {len(response)}")

TODO:
    more endpoints:
        - check details
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/payItems -- with payItemFilter and includePayees
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/deferredCompensation
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/benefitEnrollment -- activeOnly flag
        ? https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/checks
            w/ yearFilter, includeDetails,
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/checks/{id}
            check details w/ inlcudeLaborDetails
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/checks/{id}
            pay items
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/payGroups/{payGroupId}/payItems
            pay items by pay group: w/ payItemFilter
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/payroll/accumulations
            accumulated payrolls: w/ payrollId and effectiveDate filters
        ? https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/payroll
            get employee payrolls
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/garnishments
            employee garnishments
        - https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/timecardView
            timecard view - has timecardHours
        ? https://insperity.myisolved.com/rest/api/clients/{clientId}/legals/{legalId}/employees/{employeeId}/timecardData
            get timecard range by employee - startDate endDate

Len Wanger
2025
"""

import json
from functools import wraps

import requests

from insperity_rest_utils import *


BASE_URL = "https://insperity.myisolved.com/rest/api"
GET_TOKEN = f"{BASE_URL}/token"  # POST
CLIENTS = f"{BASE_URL}/clients"
LEGALS = f"{BASE_URL}/legals"
EMPLOYEES_MIN = "{base_url}/clients/{client_id}/legals/{legal_id}/employeesMinimal"
EMPLOYEES = "{base_url}/clients/{client_id}/employees"
EMPLOYEES_W_SSN = "{base_url}/clients/{client_id}/employeesWithSSN"
EMPLOYEE_TIMECARD_DATA = "{base_url}/clients/{client_id}/legals/{legal_id}/employees/{employee_id}/timecardData"

EMPLOYEE_CHECKS = "{base_url}/clients/{client_id}/legals/{legal_id}/employees/{employee_id}/checks"
EMPLOYEE_PAYROLL = "{base_url}/clients/{client_id}/legals/{legal_id}/employees/{employee_id}/payroll"

EMPLOYEE_BY_ID = "{base_url}/clients/{client_id}/legals/{legal_id}/employees/{employee_id}"


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
def get_client_info(token_dict: dict, client_code_filter: str|None=None, search_text: str|None=None) -> dict:
    # test getting client information
    headers = get_headers(token_dict['access_token'])
    params = {}

    if client_code_filter is not None:
        params['clientCodeFilter'] = client_code_filter

    if search_text is not None:
        params['searchText'] = search_text

    response = requests.get(CLIENTS, headers=headers, params=params)
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


def get_legal_id(legal_ids: dict, legal_name_substring: str|None) -> tuple[str, dict]:
    # return the first legal id that matches the name substring
    if (len(legal_ids)==1) or (legal_name_substring is None):
        return legal_ids[0]['id']
    else:
        for legal_id in legal_ids:
            if legal_name_substring in legal_id['legalName']:
                return legal_id['id']

    return None


def get_credentials(client_code: str, legal_name_substring: str|None = None):
    """
    Get access token, client ID, and legal ID -- this is the simplest way to get started
    Calling the REST API endpoints, assuming you only will be using the same legal_id (company)
    for all calls

    :param client_code:
    :param legal_name_substring:
    :return: tuple of three values: token dictionary, client ID, legal ID
    """
    token_dict = get_client_credential_token(client_code=client_code)
    client_id, legal_ids = get_client_and_legal_ids(token_dict=token_dict)
    legal_id = get_legal_id(legal_ids=legal_ids, legal_name_substring=legal_name_substring)

    return token_dict, client_id, legal_id


def process_response(url: str, headers: dict, params: dict) -> list[dict]:
    # process a simple (not multipage) response from the REST API endpoint
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(
            f"Error getting data from REST api (status={response.status_code}): {response.text}")

    return json.loads(response.content)


def process_multipage_response(url: str, headers: dict, params: dict) -> list[dict]:
    # process a multipage response from the REST API endpoint
    response_list = []

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Error getting data from REST api (status={response.status_code}): {response.text}")

        response_dict = json.loads(response.content)
        response_list += response_dict['results']

        if response_dict['nextPageUrl'] is None:
            break

        url = response_dict['nextPageUrl']

    return response_list


def get_minimal_employee_list_raw(token_dict: dict, client_id: str, legal_id: str, employee_status_filter: str|None=None) -> list[dict]:
    """
    get a raw list of minimal employee records. Each item in the list is the raw dictionary response from the REST API endpoint.

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_status_filter:
    :return: return a list of dicts of employee information with minimal employee info
    """
    headers = get_headers(token_dict['access_token'])
    params = {}

    url = EMPLOYEES_MIN.format(base_url=BASE_URL, client_id=client_id, legal_id=legal_id)

    if employee_status_filter is not None:
        params['employeeStatusFilter'] = employee_status_filter

    return process_multipage_response(url, headers, params)


def get_minimal_employee_list(token_dict: dict, client_id: str, legal_id: str, employee_status_filter: str|None=None) -> list[MinimalEmployee]:
    """
    get a list of minimal employee records. Each item in the list is an MinimalEmployee object.

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_status_filter:
    :return:
    """
    raw_list = get_minimal_employee_list_raw(token_dict, client_id, legal_id, employee_status_filter)

    employee_list = [fill_minimal_employee_record(raw_employee) for raw_employee in raw_list]
    return employee_list


def get_employee_list_raw(token_dict: dict, client_id: str, legal_id: str, employee_status_filter: str|None=None,
                      search_text: str|None = None, with_ssn: bool=False) -> list[dict]:
    """
    get a raw list of employee records. Each item in the list is the raw dictionary response from the REST API endpoint.

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_status_filter:
    :param search_text:
    :param with_ssn:
    :return: return a list of dicts of employee information (minimal employee info if minimal=True, full employee info
        if minimal=False)
    """
    headers = get_headers(token_dict['access_token'])
    params = {}

    if with_ssn is True:
        url = EMPLOYEES_W_SSN.format(base_url=BASE_URL, client_id=client_id, legal_id=legal_id)
    else:
        url = EMPLOYEES.format(base_url=BASE_URL, client_id=client_id, legal_id=legal_id)

    if employee_status_filter is not None:
        params['employeeStatusFilter'] = employee_status_filter

    if search_text is not None:
        params['searchText'] = search_text

    return process_multipage_response(url, headers, params)


def get_employee_list(token_dict: dict, client_id: str, legal_id: str, employee_status_filter: str|None=None,
                      search_text: str|None = None, with_ssn: bool=False) -> list[Employee]:
    """
    get a list of employee records. Each item in the list is an Employee object.

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_status_filter:
    :param search_text:
    :param with_ssn:
    :return: list of Employee objects
    """
    raw_list = get_employee_list_raw(token_dict=token_dict, client_id=client_id, legal_id=legal_id,
                                     employee_status_filter=employee_status_filter, search_text=search_text, with_ssn=with_ssn)

    employee_list = [fill_employee_record(raw_employee) for raw_employee in raw_list]
    return employee_list

####
# Experimental end points
####

def get_employee_timecard_data_raw(token_dict: dict, client_id: str, legal_id: str, employee_id: str,
                          start_date: date | None = None, end_date: date | None = None) -> list[dict]:
    """
    NOT WORKING!

    get a raw list of employee records. Each item in the list is the raw dictionary response from the REST API endpoint.

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_id:
    :param start_date:
    :param end_date:
    :return: return a list of dicts of employee information (minimal employee info if minimal=True, full employee info
        if minimal=False)
    """
    headers = get_headers(token_dict['access_token'])
    params = {}

    url = EMPLOYEE_TIMECARD_DATA.format(base_url=BASE_URL, client_id=client_id, legal_id=legal_id, employee_id=employee_id)

    print(f"{url=}")  # DEBUG

    if start_date is not None:
        start_date_str = start_date.isoformat()
        params['startDate'] = start_date_str

    if end_date is not None:
        end_date_str = end_date.isoformat()
        params['startDate'] = end_date_str

    return process_multipage_response(url, headers, params)


def get_employee_checks_raw(token_dict: dict, client_id: str, legal_id: str, employee_id: str,
                          year_filter: int | None = None, include_details: bool | None = None) -> list[dict]:
    """
    get a raw list of employee checks

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_id:
    :param year_filter:
    :param include_details:
    :return: return a list of dicts of employee information (minimal employee info if minimal=True, full employee info
        if minimal=False)
    """
    headers = get_headers(token_dict['access_token'])
    params = {}

    url = EMPLOYEE_CHECKS.format(base_url=BASE_URL, client_id=client_id, legal_id=legal_id, employee_id=employee_id)

    print(f"{url=}")  # DEBUG

    if year_filter is not None:
        params['yearFilter'] = year_filter

    if include_details is not None:
        params['includeDetails'] = include_details

    return process_multipage_response(url, headers, params)




def get_employee_by_id(token_dict: dict, client_id: str, legal_id: str, employee_id: str) -> list[dict]:
    """
    get employee by id

    NOTE: LOTS OF FILTERS TO IMPLEMENT

    :param token_dict:
    :param client_id:
    :param legal_id:
    :param employee_id:
    :return: return data for the employee
    """
    headers = get_headers(token_dict['access_token'])
    params = {}

    url = EMPLOYEE_BY_ID.format(base_url=BASE_URL, client_id=client_id, legal_id=legal_id, employee_id=employee_id)

    print(f"{url=}")  # DEBUG
    return process_response(url, headers, params)
