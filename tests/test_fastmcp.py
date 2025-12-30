"""
Test test_fastmcp_server

In a separate terminal, run:
    fastmcp run tests/test_fastmcp_server.py -t http -p "8080"

"""

import asyncio
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

# from test_fastmcp_server import mcp


async def get_list_tools(main_mcp_client: Client[FastMCPTransport]) -> list:
    list_tools = await main_mcp_client.list_tools()
    return list_tools


async def test_call_tool(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool("roll_dice", {"n_dice": "3"})
    return result


async def main():
    # async with main_mcp_client() as client:

    client = Client("http://localhost:8080/mcp")
    async with client:
        # resources = await client.list_resources()
        # print(f"{resources=}")

        tools = await client.list_tools()
        print(f"{tools=}")

        # result = await client.call_tool("roll_dice", {"n_dice": "3"})
        result = await test_call_tool(client)

    print(f"{result=}")
    structured_content = result.structured_content
    print(f"{structured_content['result']=}, {sum(structured_content['result'])=}")


if __name__ == "__main__":
    asyncio.run(main())
    print("done")