from backend.models import OutboundCallRequestBuilder, OutboundCallRequest


def test_outbound_call_request_builder():
    request = OutboundCallRequestBuilder().build()
    assert isinstance(request, OutboundCallRequest)
