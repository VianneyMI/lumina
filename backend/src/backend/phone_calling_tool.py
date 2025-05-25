import requests
from dotenv import load_dotenv
import os
from smolagents import Tool
from backend.models import OutboundCallRequest, OutboundCallRequestBuilder

load_dotenv()

eleven_labs_twillio_url = "https://api.elevenlabs.io/v1/convai/twilio/outbound-call"
eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")


def make_outbound_call(request: OutboundCallRequest):
    response = requests.post(
        eleven_labs_twillio_url,
        headers={"Xi-Api-Key": eleven_labs_api_key},
        json=request.model_dump(),
    )
    return response.json()


class PhoneCallingTool(Tool):
    name = "make_outbound_call"
    description = (
        "Sends a request to Twilio to make an outbound call to a phone number."
    )

    inputs = {
        "user_name": {
            "type": "string",
            "description": "The name of the user to call.",
            "default": "Vianney",
            "nullable": True,
        },
        "reminders": {
            "type": "string",
            "description": "The reminders to send to the user passed as a comma separated list as a string",
            "nullable": True,
        },
        "actions": {
            "type": "string",
            "description": "The actions to send to the user passed a comma separated list as a string",
            "nullable": True,
        },
    }

    output_type = "object"

    def forward(
        self,
        user_name: str = "Vianney",
        reminders: str | None = None,
        actions: str | None = None,
    ) -> str:
        request = (
            OutboundCallRequestBuilder()
            .with_dynamic_variables(
                {"user_name": user_name, "reminders": reminders, "actions": actions}
            )
            .build()
        )
        response = make_outbound_call(request)
        return response


if __name__ == "__main__":
    tool = PhoneCallingTool()
    print(tool.forward())
