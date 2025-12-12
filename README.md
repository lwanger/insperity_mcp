
Insperity MCP project

Python package to interact with Insperity REST API.

For examples on how to use the package, see the examples folder. The simplest example is:

```
    from dotenv import load_dotenv
    from insperity_rest_api import *

    my_client_code = 'your client code here'  

    # Get access credentials (token_dict, client_id, legal_id) to call the API endpoints
    token_dict, client_id, legal_id = get_credentials(client_code=my_client_code, legal_name_substring=None)

    # Use the access credentials to call an API endpoint
    response = get_minimal_employee_list(token_dict=token_dict, client_id=client_id, legal_id=legal_id)
```

note: don't put your client code in the script like was done above! See the examples in the
examples folder for how to use environment variables to store your client code.

The insperity_mcp package can be found on GitHub at:

    https://github.com/lwanger/insperity_mcp

Documentation for the Insperity REST API endpoints:

    http://insperity.myisolved.com/rest

TODO:

- test Insperity REST API
  - get check details (requires employee id)
  - implement additional REST API endpoints
- use FastMCP to build MCP server
- add ability to get employee profile to MCP
- make an example for NEST: get employees hired since last 120 day check,
    termed since last check, get email address and send email to employee
- 
- running locally: 
  - Goose?: https://block.github.io/goose/docs/goose-architecture/
  - https://blog.craigers.rocks/mcp-ollama/
  - or: https://github.com/Sanjaykrishnamurthy/mcp-ollama-integration
  - or: https://thomas.trocha.com/blog/creating-a-world-time-mcp-server-and-agent-with-a-local-ollama-llm-llama3-1-latest-on-linux/
  - or: https://github.com/rajeevchandra/mcp-client-server-example
  - or: https://medium.com/@techofhp/simple-mcp-tools-demo-using-fastmcp-and-a-local-llm-d266b8a166bd
  - or: https://medium.com/@smrati.katiyar/building-mcp-server-and-client-in-python-and-using-ollama-as-llm-provider-dd79fe3a2b16
- https://github.com/open-webui/open-webui


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

REST Questions:
  - way to run a report?
  - way to send a message to an employee? (using a template)
  - way to add deferred compensation to employee?