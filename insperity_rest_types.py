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

Len Wanger
2025
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Employee:
    id: str
    time_clock_id: str
    employee_number: str
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    gender: str
    marital_status: str
    address1: str
    address2: str
    city: str
    state: str
    zip_code: str
    email: str
    phone_number: str

    hire_date: date
    employee_number: str
    employment_status: str
    employee_category_code: str # e.g. "FT"
    employee_category_fulltime_equivalient: str
    employment_type: str
    pay_type: str   # e.g. "Auto Salary" "Hourly"
    assign_manager_name: str   # e.g. "Auto Salary" "Hourly"
    assign_manager_id: str   # e.g. "Auto Salary" "Hourly"

    job_id: str
    job_title: str
    work_location: str
    legal_code: str

    hourly_rate: float = 0.0
    annual_salary: float = 0.0
    ssn: str = None


if __name__ == '__main__':
    employee_1 = Employee(
        id="A001", time_clock_id='clock-0012', employee_number='0012',
        first_name='Foo', last_name='Barr', middle_name='',
        birth_date=date(1980, 1, 1), gender='M', marital_status='Married',
        address1='123 Main St',
        address2='', city='Anytown', state='NY', zip_code='12345', email='foo@bar.com',
        phone_number='888-001-1234',
        hire_date=date(2022, 1, 1),
        employment_status='Active', employee_category_code='FT', employee_category_fulltime_equivalient='Full Time',
        employment_type='Full Time', pay_type="Auto Salary",
        assign_manager_name='Scrooge McDuck', assign_manager_id='0017',
        job_id='job-001', job_title='Engineer', work_location='NY', legal_code='207001-1',
        hourly_rate= 17.5,
        ssn= None
    )

    print(employee_1)