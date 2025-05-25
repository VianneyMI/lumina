import asyncio
import json
import os
from typing import Any

import litellm
from aci import ACI
from aci.types.enums import FunctionDefinitionFormat
from agents import Agent, FunctionTool, RunContextWrapper, Runner
from dotenv import load_dotenv


from smolagents import ToolCallingAgent, LiteLLMModel, Tool

load_dotenv()
LINKED_ACCOUNT_OWNER_ID = os.getenv("LINKED_ACCOUNT_OWNER_ID", "")
if not LINKED_ACCOUNT_OWNER_ID:
    raise ValueError("LINKED_ACCOUNT_OWNER_ID is not set")

aci = ACI()

llm = LiteLLMModel("gemini/gemini-2.5-flash-preview-04-17")
litellm.drop_params = True  # 👈 KEY CHANGE


def get_tool(function_name: str, linked_account_owner_id: str) -> FunctionTool:
    function_definition = aci.functions.get_definition(function_name)
    name = function_definition["function"]["name"]
    description = function_definition["function"]["description"]
    parameters = function_definition["function"]["parameters"]

    async def tool_impl(ctx: RunContextWrapper[Any], args: str) -> str:
        return aci.handle_function_call(
            function_name,
            json.loads(args),
            linked_account_owner_id=linked_account_owner_id,
            allowed_apps_only=True,
            format=FunctionDefinitionFormat.OPENAI,
        )

    class GmailTool(Tool):
        name = name
        description = description

    return FunctionTool(
        name=name,
        description=description,
        params_json_schema=parameters,
        on_invoke_tool=tool_impl,
        # strict_json_schema=True,
    )


gmail_agent = ToolCallingAgent(
    name="gmail_agent",
    # model="o1",
    instructions="You are a helpful assistant that can use available tools to help the user.",
    tools=[
        get_tool("GMAIL__MESSAGES_LIST", LINKED_ACCOUNT_OWNER_ID),
        get_tool("GMAIL__MESSAGES_GET", LINKED_ACCOUNT_OWNER_ID),
    ],
)


async def main() -> None:
    try:
        result = await Runner.run(
            starting_agent=gmail_agent,
            input="Search for emails from vianney.mixtur@outlook.fr, read the access code in its last email",
        )
        print(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
