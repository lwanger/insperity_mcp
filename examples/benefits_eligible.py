"""
Example of calling the Insperity REST API using the insperity_mcp package to find employees who are eligible for benefits.

    - status == active
    - type is salaried, or FT equiv. (hourly with >= 30 hrs per week)
    - get name and email
    - save to CSV file

Len Wanger
2025
"""

from dotenv import load_dotenv

from insperity_rest_types import Employee
from insperity_rest_utils import fill_employee_record
from insperity_rest_api import *


if __name__ == '__main__':
    eligible_employees = []

    # load environment variables from .env file, such as client_code and api secret
    load_dotenv()

    #  You will want to use your own values for the LEGAL_ID and legal_name_substring variables
    legal_id_ves = os.getenv('LEGAL_ID_VES')

    # Get access credentials (token_dict, client_id, legal_id) to call the API endpoints
    token_dict, client_id, legal_id = get_credentials(client_code=legal_id_ves, legal_name_substring=None)

    # call the employees API endpoint to get a list of employees
    # response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, employee_status_filter="Active")
    response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id)

    # print number of employees returned and first employee details
    print(f"get_minimal_employee_list: number of employees returned: {len(response)}")

    for employee_dict in response:
        empl = fill_employee_record(employee_dict)

    if len(response) > 0:
        employee = response[0]
        first_name = employee['firstName']
        last_name = employee['lastName']
        employee_number = employee['employeeNumber']
        employment_status = employee['employmentStatus']

        print(f"Employee 0: first name: {first_name=} last name: {last_name=} employee number: {employee_number=} employee status {employment_status=}")

    print("\nDone!")