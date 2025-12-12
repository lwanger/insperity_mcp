"""
Simple example to get a list of emails for employees matching a name.

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

    # Get search term from user
    while True:
        print("\n\n")
        search_text = ""

        while True:
            search_text = input("Please enter a search term to use to find employees (e.g. last name): ")
            if len(search_text) > 0:
                print(f"\nSearching for employees with name containing: {search_text}")
                break
            else:
                print("\tSearch term cannot be empty. Please try again.")

        # call the employees API endpoint to get a list of matching employees
        retrieved_employees = get_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id, search_text=search_text)

        # print details of matching employees
        print(f"Number of employees returned: {len(retrieved_employees)}\n")
        print("\nname\t\t\temail\t\t\t\t\tphone number")

        for employee in retrieved_employees:
            use_middle_name = f"{employee.middle_name} " if employee.middle_name is not None else " "
            print(f"{employee.first_name}{use_middle_name}{employee.last_name}\t\t{employee.email}\t\t\t{employee.phone_number}")

        answer = input("\nSearch again? (y/n)")
        if answer.lower() != 'y':
            break

    print("\nDone!")