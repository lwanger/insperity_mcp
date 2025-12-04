"""
Test getting refresh tokens.

Loop until access token expires, then get new refresh token.

refresh_token_decorator_test tests using the refresh token decorator. This decorator wraps a function that calls a REST
 API endpoint will automatically refresh an expired access token and automatically retry the call if the access token
 expires.

Len Wanger
2025
"""

import asyncio

from dotenv import load_dotenv

from insperity_rest_api import *

SLEEP_TIME = 60  # number of seconds to sleep between requests

async def async_sleep(seconds):
    await asyncio.sleep(seconds)


@refresh_token
def get_client_info_refresh() -> dict:
    # test getting client information
    headers = get_headers(token_dict['access_token'])
    response = requests.get(CLIENTS, headers=headers)
    return response


def refresh_token_test(token_dict):
    total_sleep_time = 0
    legal_id_ves = os.getenv('LEGAL_ID_VES')

    while True:
        try:
            _ = get_client_id(token_dict)
            print(f"{total_sleep_time=} seconds")
            asyncio.run(async_sleep(SLEEP_TIME))
            total_sleep_time += SLEEP_TIME
        except Exception as e:
            print("got an exception!")
            token_dict = get_refresh_token(client_code=legal_id_ves, token_dict=token_dict)
            print(f"new access token: {token_dict['access_token']}")


def refresh_token_decorator_test(token_dict: dict):
    total_sleep_time = 0

    while True:
        try:
            access_token = token_dict['access_token']
            _ = get_client_info_refresh(token_dict=token_dict)

            if token_dict['access_token'] != access_token:
                print("access token changed")

            print(f"{total_sleep_time=} seconds")
            asyncio.run( async_sleep(SLEEP_TIME) )
            total_sleep_time += SLEEP_TIME
        except Exception as e:
            print("refresh_token_decorator_test: got an exception!")


def get_client_info_test(token_dict: dict):
    total_sleep_time = 0

    while True:
        try:
            access_token = token_dict['access_token']
            _ = get_client_id(token_dict=token_dict)

            if token_dict['access_token'] != access_token:
                print("access token changed")

            print(f"{total_sleep_time=} seconds")
            asyncio.run( async_sleep(SLEEP_TIME) )
            total_sleep_time += SLEEP_TIME
        except Exception as e:
            print("refresh_token_decorator_test: got an exception!")


if __name__ == '__main__':
    load_dotenv()
    legal_id_ves = os.getenv('LEGAL_ID_VES')
    token_dict = get_client_credential_token(client_code=legal_id_ves)

    client_id, legal_ids = get_client_and_legal_ids(token_dict)
    legal_id, legal_links = get_legal_id(legal_ids, 'Newport')

    if False:
        # test fetching refresh token
        print("calling refresh token test...")
        refresh_token_test(token_dict)
    elif False:
        # test using the refresh token decorator
        print("calling refresh token decorator test...")
        refresh_token_decorator_test(legal_id_ves, token_dict)
    else:
        # test using the version in insperity_rest_api.py
        print("calling get client info test...")
        get_client_info_test(token_dict)