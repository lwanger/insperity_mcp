
Insperity MCP project

Python package to interact with Insperity REST API.

For examples on how to use the package, see the tests folder.

TODO:

- test Insperity REST API
  - employee list: add filters: giuser id
  - get check details (requires employee id)
  - implement additional REST API endpoints
- use FastMCP to build MCP server
- add ability to get employee profile to MCP
- make an example for NEST: get employees hired since last 120 day check,
    termed since last check, get email address and send email to employee

python-dotenv is used to manage environment variables, including API credentials. Variables,
such as API credentials, should be stored in a .env file. Dotenv will automatically load variables
from a .env file, where they will be available as environment variables. Environment variables
should be named as follows:

- INSPERITY_CLIENT_ID = api_client_id
- INSPERITY_SECRET = api_secret
- INSPERITY_USER = insperity_username
- INSPERITY_PWD = insperity_username

It is also useful to put the legal id for any entities to access:

- LEGAL_ID_1 = legal_id_for_company_1
- LEGAL_ID_2 = legal_id_for_company_2

Len Wanger
2025