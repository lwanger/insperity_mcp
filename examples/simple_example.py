"""
Simple example of calling the Insperity REST API using the insperity_mcp package.

This example gets the access token, client ID, and legal ID, then calls the API endpoint to get a list of employees and
prints some of the first employee's details.

Documentation for the Insperity REST API endpoints:

    http://insperity.myisolved.com/rest

All of the API calls require a token_dict (containing access_token and refresh_token) and client_id and most
require a legal_id. If you are only using one legal_id for all calls, you can use the get_credentials function to
get all three values for you (as done below). If not, you can use the get_client_and_legal_ids function to get the
client_id and then use the get_legal_id function to get the legal_id for a particular legal company.

Len Wanger
2025
"""

from dotenv import load_dotenv

from insperity_rest_api import *


if __name__ == '__main__':
    # load environment variables from .env file, such as client_code and api secret
    load_dotenv()

    #  You will want to use your own values for the LEGAL_ID and legal_name_substring variables
    legal_id_ves = os.getenv('LEGAL_ID_VES')

    # Get access credentials (token_dict, client_id, legal_id) to call the API endpoints
    token_dict, client_id, legal_id = get_credentials(client_code=legal_id_ves, legal_name_substring=None)

    # call the employees API endpoint to get a list of employees
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