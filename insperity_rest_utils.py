"""
Utility functions used by Insperity REST API

https://insperity.myisolved.com/rest

Len Wanger
2025
"""

import base64
from datetime import datetime, date
import os

from insperity_rest_types import Employee, MinimalEmployee

##############################################################################################################
# Utility routines used by endpoints
##############################################################################################################
def to_mime_base64(input_string: str) -> str:
    # Convert a string to RFC2045-MIME variant of Base64.
    byte_data = input_string.encode("utf-8")
    mime_encoded = base64.b64encode(byte_data)
    return mime_encoded.decode("utf-8")


def get_combined_key() -> str:
    # create combined key used in header for REST API calls
    return to_mime_base64(f"{os.getenv('INSPERITY_CLIENT_ID')}:{os.getenv('INSPERITY_SECRET')}")


def get_headers(access_token: str, essScope: str="Employee") -> dict:
    # create header dictionary used by requests for REST API calls
    return {
        'Authorization': f"Bearer {access_token}",
        'essScope': essScope  # ?essScope={Employee|Manager|Supervisor|All*}
    }


def string_to_date(date_str: str) -> date:
    try:
        return datetime.fromisoformat(date_str).date()
    except TypeError:
        return None


def fill_employee_record(employee_dict: dict) -> Employee:
    # create an Employee object from dictionary returned by get_employees
    new_dict = {
        'id': employee_dict['id'],
        'first_name': employee_dict['nameAddress']['firstName'],
        'last_name': employee_dict['nameAddress']['lastName'],
        'middle_name': employee_dict['nameAddress']['middleName'],
        'address1': employee_dict['nameAddress']['address1'],
        'address2': employee_dict['nameAddress']['address2'],
        'city': employee_dict['nameAddress']['city'],
        'state': employee_dict['nameAddress']['state'],
        'zip_code': employee_dict['nameAddress']['zipCode'],
        'employee_number': employee_dict['employeeNumber'],
        'employment_status': employee_dict['employmentStatus'],
        'phone_number': employee_dict['personal']['homePhone'],
        'email': employee_dict['emailAddress'],
        'birth_date': string_to_date(employee_dict['birthDate']),  # convert to date (str, eg "2019-01-01T00:00:00")
        'employment_category_code': employee_dict['employmentCategoryCode'],  #(e.g. "FT")
        'employment_category_fulltime_equivalent': employee_dict['employmentCategoryFullTimeEquivalent'],
        'hire_date': string_to_date(employee_dict['hireDate']),  # convert to date (str, eg "2019-01-01T00:00:00")
        'job_id': employee_dict['jobId'],
        'job_title': employee_dict['jobTitle'],
        'marital_status': employee_dict['maritalStatus'],
        'pay_type': employee_dict['payType'],  # e.g. "Auto Salary" "Hourly"
        'time_clock_id': employee_dict['timeclockId'],
        'ssn': employee_dict['ssn'],
        'work_location': employee_dict['workLocation'],
        'legal_code': employee_dict['legalCode'],  # eg "'2502007-1'
    }

    new_dict['gender'] = employee_dict.get('gender', None)

    hourly_rate = employee_dict.get('hourlyRate', None)
    if hourly_rate is not None:
        new_dict['hourly_rate'] = float(hourly_rate)

    annual_salary = employee_dict.get('annualSalary', None)
    if annual_salary is not None:
        new_dict['annual_salary'] = float(annual_salary)

    if 'assignedManager' in employee_dict:
        new_dict['assigned_manager_name'] = employee_dict['assignedManager']['employeeName'],
        new_dict['assigned_manager_id'] = employee_dict['assignedManager']['id'],
    else:
        new_dict['assigned_manager_name'] = new_dict['assigned_manager_id'] = None

    return Employee(**new_dict)


def fill_minimal_employee_record(employee_dict: dict) -> Employee:
    # create a MinimalEmployee object from dictionary returned by get_employees
    new_dict = {
        'id': employee_dict['id'],
        'formal_name': employee_dict['formalName'],
        'first_name': employee_dict['firstName'],
        'last_name': employee_dict['lastName'],
        'middle_initial': ['middleInitial'],
        'city': employee_dict['city'],
        'state': employee_dict['state'],
        'employee_number': employee_dict['employeeNumber'],
        'employment_status': employee_dict['employmentStatus'],
        'email': employee_dict['selfServiceEmail'],
        'hire_date': string_to_date(employee_dict['hireDate']),  # convert to date (str, eg "2019-01-01T00:00:00")
        'time_clock_id': employee_dict['timeclockId'],
    }

    new_dict['is_manager'] = employee_dict.get('isManager', None)
    new_dict['is_supervisor'] = employee_dict.get('isSupervisor', None)
    new_dict['job_code'] = employee_dict.get('job_code', None)
    new_dict['job_title'] = employee_dict.get('jobTitle', None)

    return MinimalEmployee(**new_dict)
