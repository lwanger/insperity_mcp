"""
Example of calling the Insperity REST API using the insperity_mcp package to find employees who are eligible for benefits.

    X status == active
    - type is salaried, or FT equiv. (hourly with >= 30 hrs per week)
    - get name and email
    - save to CSV file

Len Wanger
2025
"""
from tarfile import fully_trusted_filter

from dotenv import load_dotenv

from insperity_rest_api import *


if __name__ == '__main__':
    eligible_employees = []

    # load environment variables from .env file, such as client_code and api secret
    load_dotenv()

    #  You will want to use your own values for the LEGAL_ID and legal_name_substring variables
    legal_id_ves = os.getenv('LEGAL_ID_VES')

    # Get access credentials (token_dict, client_id, legal_id) to call the API endpoints
    token_dict, client_id, legal_id = get_credentials(client_code=legal_id_ves, legal_name_substring=None)

    full_employee_list = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, employee_status_filter="Active")
    employee_list = []

    for employee in full_employee_list:
        if 'salary' in employee.employment_category_code.lower():
            employee_list.append(employee)
        else:
            # 30 hrs per week average?
            pass

        # check if averaging 30 hours per week
        # if employee.average_hours_per_week >= 30:


    print(f"Found {len(employee_list)} employees eligible for benefits.")
    print("\nDone!")