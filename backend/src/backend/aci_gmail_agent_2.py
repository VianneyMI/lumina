from smolagents import ToolCallingAgent, Tool, LiteLLMModel
from aci import ACI
from aci.types.enums import FunctionDefinitionFormat
import litellm
from typing import Any

llm = LiteLLMModel("anthropic/claude-3-5-sonnet-latest")
litellm.drop_params = True  # 👈 KEY CHANGE


aci = ACI()

gmail_list_messages_function_definition = aci.functions.get_definition(
    "GMAIL__MESSAGES_LIST"
)
gmail_get_message_function_definition = aci.functions.get_definition(
    "GMAIL__MESSAGES_GET"
)


class GmailListMessagesTool(Tool):
    name = gmail_list_messages_function_definition["function"]["name"]
    description = """List the messages in my gmail account."""
    inputs = {
        "q": {
            "type": "string",
            "description": "The query to search for, e.g. 'from:vianney.mixtur@outlook.fr'",
        },
        # "maxResults": {
        #     "type": "integer",
        #     "description": "The maximum number of results to return, e.g. 10. Default is 100. Max is 500.",
        #     "default": 100,
        # },
        # "labelIds": {
        #     "type": "array",
        #     "description": "The label ids to include in the results. Default is ['INBOX'].",
        #     "default": ["INBOX"],
        # },
        # "pageToken": {
        #     "type": "string",
        #     "description": "The page token to use for pagination",
        # },
        # "includeSpamTrash": {
        #     "type": "boolean",
        #     "description": "Whether to include spam and trash in the results. Default is False.",
        #     "default": False,
        # },
    }
    output_type = "object"

    def forward(
        self,
        q: str,
        # maxResults: int,
        # labelIds: list[str],
        # pageToken: str,
        # includeSpamTrash: bool,
    ) -> dict:
        return aci.handle_function_call(
            self.name,
            {
                "query": {
                    "q": q,
                    # "maxResults": maxResults,
                    # "labelIds": labelIds,
                    # "pageToken": pageToken,
                    # "includeSpamTrash": includeSpamTrash,
                }
            },
            linked_account_owner_id="HACKATHON",
            allowed_apps_only=True,
            format=FunctionDefinitionFormat.OPENAI,
        )


class GmailGetMessageTool(Tool):
    name = gmail_get_message_function_definition["function"]["name"]
    description = gmail_get_message_function_definition["function"]["description"]
    inputs = {
        "path": {
            "type": "object",
            "description": "A path object containing the id key. id being the id of the message to get, e.g. '1234567890'",
        },
        "query": {
            "type": "object",
            "description": """
             A query object containing the following keys:
             - format: the desired return format can be either "full", "metadata", "minimal" or "raw". Default is "full".
             - metatadaHeaders: a list of metadata headers to include in the response.

            """,
        },
    }
    output_type = "object"

    def forward(self, path: dict[str, Any], query: dict[str, Any]) -> dict:
        return aci.handle_function_call(
            self.name,
            {"path": path, "query": query},
            linked_account_owner_id="HACKATHON",
            allowed_apps_only=True,
            format=FunctionDefinitionFormat.OPENAI,
        )


agent = ToolCallingAgent(
    name="gmail_agent",
    model=llm,
    # instructions="You are a helpful assistant that can use available tools to help the user.",
    tools=[GmailListMessagesTool(), GmailGetMessageTool()],
    add_base_tools=True,
)


def main() -> None:
    result = agent.run(
        "Examine my last 10 emails. There should be one from vianney.mixtur@outlook.fr. Read the confirmation code in the email and return it."
    )


if __name__ == "__main__":
    main()
