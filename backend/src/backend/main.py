import requests
from dotenv import load_dotenv
import os
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


def main():
    request = OutboundCallRequestBuilder().build()
    response = make_outbound_call(request)
    print(response)


if __name__ == "__main__":
    main()
