"""
Utility functions used by Insperity REST API

https://insperity.myisolved.com/rest

Len Wanger
2025
"""

import base64
from datetime import datetime, date
import os

from insperity_rest_types import Employee

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


def get_headers(access_token: str) -> dict:
    # create header dictionary used by requests for REST API calls
    return {
        'Authorization': f"Bearer {access_token}",
        'essScope': "Employee"  # ?essScope={Employee|Manager|Supervisor|All*}
    }


def string_to_date(date_str: str) -> date:
    dt = datetime.fromisoformat(date_str)
    return dt.date()


def fill_employee_record(employee_dict: dict) -> Employee:
    new_dict = {
        'id': employee_dict['id'],
        'first_name': employee_dict['firstName'],
        'last_name': employee_dict['lastName'],
        'middle_name': employee_dict['middleName'],
        'gender': employee_dict['gender'],

        'address1': employee_dict['nameAddress']['address1'],
        'address2': employee_dict['nameAddress']['address2'],
        'city': employee_dict['nameAddress']['city'],
        'state': employee_dict['nameAddress']['state'],
        'zip_code': employee_dict['nameAddress']['zipCode'],

        'employee_number': employee_dict['employeeNumber'],
        'employment_status': employee_dict['employmentStatus'],
        'phone_number': employee_dict['personal']['homePhone'],
        'email': employee_dict['emailAddress'],
        'birth_date': string_to_date(employee_dict['birthdate']),  # convert to date (str, eg "2019-01-01T00:00:00")
        'employee_category_code': employee_dict['employeeCategoryCode'],  #(e.g. "FT")
        'employee_category_fulltime_equivalient': employee_dict['employeeCategoryFullTimeEquivalient'],
        'employment_type': employee_dict['employmentType'],  # (e.g. "Full Time")

        'hire_date': string_to_date(employee_dict['hireDate']),  # convert to date (str, eg "2019-01-01T00:00:00")
        'hourly_rate': float( employee_dict['hourlyRate'] ), # convert to float
        'annual_salary': float( employee_dict['annualSalary'] ), # convert to float
        'job_id': employee_dict['jobId'],
        'job_title': employee_dict['jobTitle'],
        'marital_status': employee_dict['maritalStatus'],
        'pay_type': employee_dict['payType'],  # e.g. "Auto Salary" "Hourly"
        'time_clock_id': employee_dict['timeClockId'],
        'ssn': employee_dict['ssn'],
        'work_location': employee_dict['workLocation'],
        'legal_code': employee_dict['legalCode'],  # eg "'2502007-1'
        'assign_manager_name': employee_dict['assignedManager']['employeeName'],
        'assign_manager_id': employee_dict['assignedManager']['id'],
    }

    return Employee(**new_dict)
