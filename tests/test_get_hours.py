"""
Test new endpoints to get hours worked by employee.

Error:



url='https://insperity.myisolved.com/rest/api/clients/5660/legals/6752/employees/407924/timecardData'
"{"message":"No HTTP resource was found that matches the request URI

'https://insperity.myisolved.com/rest/api/clients/5660/legals/6752/employees/407924/timecardData'."}"

'https://insperity.myisolved.com/rest/api/clients/5660/legals/6751/employees/407924/timecardData'."}"

'https://insperity.myisolved.com/rest/api/clients/5660/legals/6752/employees/407924/checks'
'{"message":"Authorization has been denied for this request."}'

'https://insperity.myisolved.com/rest/api/clients/5660/legals/6751/employees/407924/checks'
'{"message":"Authorization has been denied for this request."}'


Len Wanger
2025
"""

from dotenv import load_dotenv

from insperity_rest_api import *


# def get_employee_id():
#     pass


if __name__ == '__main__':
    # initialize REST API credentials
    load_dotenv()
    legal_id_ves = os.getenv('LEGAL_ID_VES')
    legal_id_npt = os.getenv('LEGAL_ID_NPT')

    # token_dict, client_id, legal_id = get_credentials(client_code=legal_id_ves, legal_name_substring=None)
    token_dict, client_id, legal_id = get_credentials(client_code=legal_id_npt, legal_name_substring="Newport")

    response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, search_text="Neace")
    # response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, search_text="Deane")
    employee_id = response[0].id

    # response = get_employee_list_raw(token_dict=token_dict, client_id=client_id, legal_id=legal_id, search_text="Neace")
    # employee_id = response[0]['employeeNumber']  # in raw
    # employee_id = response[0]['timeclockId']  # in raw
    # employee_id = response[0]['personal']['id']  # in raw

    # tests to get hours worked by employee..... EXPERIMENTAL
    # no match? wrong ID? wrong legal?
    response = get_employee_timecard_data_raw(token_dict, client_id, legal_id, employee_id, start_date=None, end_date=None)
    # response = get_employee_timecard_data_raw(token_dict, client_id, legal_id, employee_id, start_date=None, end_date=None)
    response = get_employee_checks_raw(token_dict, client_id, legal_id, employee_id, year_filter=None, include_details=None)
    # response = get_employee_checks_raw(token_dict, client_id, legal_id, employee_id, year_filter=None, include_details=None)
    print(response[0])

    print("\nDone!")