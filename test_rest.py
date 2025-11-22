"""
Test Insperity REST API

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
    - implement request of refresh token
    - handle paginated results
    - test calling links from legal_links
    - move constants to another file
    - safety: check return statuses and do error checking!
"""

import base64
import json
import os

from dotenv import load_dotenv
import requests

from insperity_rest_api import *

LEGAL_ID_VES = '2502007-1'
LEGAL_ID_NPT = '2502007-2'
LEGAL_ID_LV = '2502007-3'


if __name__ == '__main__':
    load_dotenv()
    access_token = get_client_credential_token(client_code=LEGAL_ID_VES)

    # test using the token
    # results = get_client_info(access_token)
    # print(f"{results[0]['clientCode']=}: {results[0]['clientName']=}")

    # client_id = get_client_id(access_token)
    # print(f"{client_id=}")

    # legal_ids = get_legals(access_token)
    # print(f"{legal_ids=}")

    client_id, legal_ids = get_client_and_legal_ids(access_token)
    legal_id, legal_links = get_legal_id(legal_ids, 'Newport')
    print(f"{client_id=} {legal_id=}, {legal_links=}")

    response = get_employee_list(access_token, client_id, legal_id, minimal=True)
    print(f"number of employees returned: {len(response)}")
