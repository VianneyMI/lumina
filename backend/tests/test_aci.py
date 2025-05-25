import json
from pathlib import Path

from aci import ACI
from aci.types.functions import FunctionDefinitionFormat
from dotenv import load_dotenv

path_to_definitions = (
    Path(__file__).parents[1] / "src" / "backend" / "aci_functions_definitions"
)
load_dotenv()


def test_aci_functions_get_definition():
    aci = ACI()
    brave_search_function_definition = aci.functions.get_definition(
        "BRAVE_SEARCH__WEB_SEARCH"
    )

    gmail_messages_list_function_definition = aci.functions.get_definition(
        "GMAIL__MESSAGES_LIST"
    )

    gmail_messages_get_function_definition = aci.functions.get_definition(
        "GMAIL__MESSAGES_GET"
    )

    with open(path_to_definitions / "brave_search_web_search.json", "w") as f:
        json.dump(brave_search_function_definition, f)

    with open(path_to_definitions / "gmail_messages_list.json", "w") as f:
        json.dump(gmail_messages_list_function_definition, f)

    with open(path_to_definitions / "gmail_messages_get.json", "w") as f:
        json.dump(gmail_messages_get_function_definition, f)

    assert brave_search_function_definition is not None
    assert gmail_messages_list_function_definition is not None
    assert gmail_messages_get_function_definition is not None


def test_aci_handle_function_call():
    aci = ACI()
    # brave_search_function_definition = aci.functions.get_definition(
    #     "BRAVE_SEARCH__WEB_SEARCH"
    # )

    query = {"query": {"q": "Aipolabs ACI"}}

    result = aci.handle_function_call(
        "BRAVE_SEARCH__WEB_SEARCH",
        query,
        linked_account_owner_id="HACKATHON",
        allowed_apps_only=True,
        format=FunctionDefinitionFormat.OPENAI,
    )

    assert result is not None
