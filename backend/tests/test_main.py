from backend.models import OutboundCallRequestBuilder, OutboundCallResponse
from backend.main import make_outbound_call


def test_make_outbound_call() -> None:
    request = OutboundCallRequestBuilder().build()
    response_json = make_outbound_call(request)
    response = OutboundCallResponse(**response_json)
    assert response.success
