from pydantic import BaseModel
from typing import Any


AGENT_ID = "agent_01jw16cknyetgr98rpd790k7je"
AGENT_PHONE_NUMBER_ID = "phnum_01jw1ddgmyfagvqxw4fqvftbaj"
TO_NUMBER = "+33601267620"

DYNAMIC_VARIABLES = {
    "actions": ["Remind Vianney about mother's day happening tomorrow"]
}


class AgentPrompt(BaseModel):
    prompt: str | None = None


class AgentConfig(BaseModel):
    prompt: AgentPrompt = AgentPrompt()
    first_message: str | None = None
    language: str | None = None


class TTSConfig(BaseModel):
    voice: str | None = None


class ConversationConfigOverride(BaseModel):
    agent: AgentConfig = AgentConfig()
    tts: TTSConfig = TTSConfig()


class ConversationInitiationClientData(BaseModel):
    conversation_config_override: ConversationConfigOverride | None = None
    custom_llm_extra_body: dict[str, Any] | None = None
    dynamic_variables: dict[str, Any] | None = None


class OutboundCallRequest(BaseModel):
    agent_id: str
    agent_phone_number_id: str
    to_number: str
    conversation_initiation_client_data: ConversationInitiationClientData | None = None


class OutboundCallResponse(BaseModel):
    success: bool
    message: str
    conversation_id: str | None = None
    callSid: str | None = None


class OutboundCallRequestBuilder(BaseModel):
    agent_id: str = AGENT_ID
    agent_phone_number_id: str = AGENT_PHONE_NUMBER_ID

    def build(self) -> OutboundCallRequest:
        return OutboundCallRequest(
            agent_id=self.agent_id,
            agent_phone_number_id=self.agent_phone_number_id,
            to_number=TO_NUMBER,
            conversation_initiation_client_data=ConversationInitiationClientData(
                dynamic_variables=DYNAMIC_VARIABLES,
            ),
        )
