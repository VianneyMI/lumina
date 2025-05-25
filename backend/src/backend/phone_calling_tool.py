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
        "irrelevant": {
            "type": "string",
            "description": "This input is not used. It is just a placeholder to make the tool work.",
        }
    }

    output_type = "object"

    def forward(self, irrelevant: str) -> str:
        request = OutboundCallRequestBuilder().build()
        response = make_outbound_call(request)
        return response
