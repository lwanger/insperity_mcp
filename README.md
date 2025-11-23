
Insperity MCP project


TODO:

- test Insperity REST API
  - employee list: add filters: status, search text, ssn filter, user id
  - get check details (requires employee id)
- use FastMCP to build MCP server
- add ability to get employee profile to MCP
- make an example for NEST: get employees hired since last 120 day check,
    termed since last check, get email address and send email to employee

python-dotenv is used to store environment variables, including API credentials.

- INSPERITY_CLIENT_ID = api_client_id
- INSPERITY_SECRET = api_secret