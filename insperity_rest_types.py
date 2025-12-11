"""
Types/Classes used for calling the Insperity REST API endpoints

Len Wanger
2025
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class MinimalEmployee:
    id: str
    time_clock_id: str
    employee_number: str
    formal_name: str
    first_name: str
    last_name: str
    middle_initial: str
    city: str
    state: str
    email: str
    hire_date: date
    employment_status: str
    is_manager: str
    is_supervisor: str
    job_code: str
    job_title: str


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
    employment_status: str
    employment_category_code: str # e.g. "FT"
    employment_category_fulltime_equivalent: str
    pay_type: str   # e.g. "Auto Salary" "Hourly"
    assigned_manager_name: str   # e.g. "Auto Salary" "Hourly"
    assigned_manager_id: str   # e.g. "Auto Salary" "Hourly"
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
        employment_status='Active', employment_category_code='FT', employment_category_fulltime_equivalent='Full Time',
        pay_type="Auto Salary", assigned_manager_name='Scrooge McDuck', assigned_manager_id='0017',
        job_id='job-001', job_title='Engineer', work_location='NY', legal_code='207001-1',
        hourly_rate= 17.5,
        ssn= None
    )

    print(employee_1)