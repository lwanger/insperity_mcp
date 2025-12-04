"""
Simple example of calling the Insperity REST API using the insperity_mcp package.

This example gets the access token, client ID, and legal ID, then calls the API endpoint to get a list of employees and
prints some of the first employee's details.

Documentation for the Insperity REST API endpoints:

    http://insperity.myisolved.com/rest

Len Wanger
2025
"""

from dotenv import load_dotenv

from insperity_rest_api import *


if __name__ == '__main__':
    # load environment variables from .env file, such as client_code and api secret
    load_dotenv()

    # get access token, client ID, and legal ID
    legal_id_ves = os.getenv('LEGAL_ID_VES')
    token_dict = get_client_credential_token(client_code=legal_id_ves)

    client_id, legal_ids = get_client_and_legal_ids(token_dict=token_dict)
    legal_id, legal_links = get_legal_id(legal_ids=legal_ids, legal_name_substring='Vegas')

    # call the API endpoint to get a list of employees
    response = get_minimal_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id)

    # print number of employees returned and first employee details
    print(f"get_minimal_employee_list: number of employees returned: {len(response)}")

    if len(response) > 0:
        employee = response[0]
        first_name = employee['firstName']
        last_name = employee['lastName']
        employee_number = employee['employeeNumber']
        employment_status = employee['employmentStatus']

        print(f"Employee 0: first name: {first_name=} last name: {last_name=} employee number: {employee_number=} employee status {employment_status=}")

    print("\nDone!")