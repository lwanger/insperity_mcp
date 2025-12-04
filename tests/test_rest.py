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
    - add filters to employee endpoints
    - implement pay endpoints
"""

from dotenv import load_dotenv

from insperity_rest_api import *


if __name__ == '__main__':
    load_dotenv()

    legal_id_ves = os.getenv('LEGAL_ID_VES')
    legal_id_lv = os.getenv('LEGAL_ID_LV')

    token_dict = get_client_credential_token(client_code=legal_id_ves)
    # token_dict = get_client_credential_token(client_code=legal_id_lv)

    # test using the token
    print("Call get_client_info:\n")
    results = get_client_info(token_dict=token_dict)
    print(f"get_client_info: {results[0]['clientCode']=}: {results[0]['clientName']=}")

    client_code_filter = legal_id_lv
    results = get_client_info(token_dict=token_dict, client_code_filter=client_code_filter)
    print(f"get_client_info w/ clientCodeFilter={client_code_filter}: {results[0]['clientCode']=}: {results[0]['clientName']=}")

    search_text = "Newport"
    results = get_client_info(token_dict=token_dict, search_text=search_text)
    print(f"get_client_info w/ clientCodeFilter={client_code_filter}: {results[0]['clientCode']=}: {results[0]['clientName']=}")

    print("")

    client_id = get_client_id(token_dict=token_dict)
    print(f"{client_id=}")

    legal_ids = get_legals(token_dict=token_dict)
    print(f"{legal_ids=}")

    client_id, legal_ids = get_client_and_legal_ids(token_dict=token_dict)
    legal_id, legal_links = get_legal_id(legal_ids=legal_ids, legal_name_substring='Vegas')
    print(f"{client_id=} {legal_id=}, {legal_links=}")

    print("Call get_employee_list tests:\n")

    response = get_minimal_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id)
    print(f"get_minimal_employee_list: number of employees returned: {len(response)}")

    response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id)
    print(f"get_employee_list: number of employees returned: {len(response)}")

    status_filter = "Active" #  "Terminated"
    response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, employee_status_filter=status_filter)
    print(f"get_employee_list w/ employee_status_filter={status_filter}: number of employees returned: {len(response)}")

    status_filter = "Terminated"
    response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id,
                                 employee_status_filter=status_filter, with_ssn=True)
    print(f"get_employee_list w/ employee_status_filter={status_filter} w ssn: number of employees returned: {len(response)}")

    search_text = "Clayton"
    # search_text = "Jimenez"
    response = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, search_text=search_text)
    print(f"get_employee_list w/ search_text={search_text}: number of employees returned: {len(response)}")
