"""
Test getting refresh tokens.

Loop until access token expires.

TODO:
    - get refresh token

Len Wanger
2025
"""

import asyncio

from dotenv import load_dotenv

from insperity_rest_api import *

LEGAL_ID_VES = '2502007-1'
SLEEP_TIME = 60  # number of seconds to sleep between requests

async def async_sleep(seconds):
    await asyncio.sleep(seconds)


if __name__ == '__main__':
    load_dotenv()
    access_token, refresh_token = get_client_credential_token(client_code=LEGAL_ID_VES)

    client_id, legal_ids = get_client_and_legal_ids(access_token)
    legal_id, legal_links = get_legal_id(legal_ids, 'Newport')

    total_sleep_time = 0

    while True:
        try:
            client_id = get_client_id(access_token)
            print(f"{total_sleep_time=} seconds")
            asyncio.run( async_sleep(SLEEP_TIME) )
            total_sleep_time += SLEEP_TIME
        except Exception as e:
            print("got an exception!")
            access_token, refresh_token = get_refresh_token(client_code=LEGAL_ID_VES, refresh_token=refresh_token)
            print(f"new refresh token: {access_token}")